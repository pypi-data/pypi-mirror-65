# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Interaction with Git repos.

It is not expected that the rise of the HGitaly project would remove
all interesting things to do with Git.
"""
from dulwich.protocol import ZERO_SHA
from hgext3rd.topic.constants import extrakey
from hggit.git_handler import GitHandler
from heptapod import gitlab
from mercurial.i18n import _
from mercurial.node import hex
from mercurial import (
    error,
    hg,
    obsutil,
    phases,
    pycompat,
)
import re
import traceback


class MultipleDescendants(LookupError):
    pass


class InvalidRef(ValueError):
    pass


def git_branch_ref(branch):
    return 'refs/heads/' + branch


def parse_git_branch_ref(ref):
    """Parse a Git branch ref for named branch and topic information

    Return ``None`` if ``ref`` is not a Git branch. This is considered
    to be a normal case::

      >>> parse_git_branch_ref("refs/tags/v1.2.3") is None
      True

    Example with a topical GitLab branch::

      >>> parse_git_branch_ref("refs/heads/topic/default/thetop")
      ('default', 'thetop')

    For named branches, the returned topic is ``None``. Checking for `None`
    is the normal way for downstream code to know if this is a topic or not::

      >>> parse_git_branch_ref("refs/heads/branch/default")
      ('default', None)

    Special case: forward slashes are considered part of the named branch::

      >>> parse_git_branch_ref("refs/heads/branch/ze/branch")
      ('ze/branch', None)

      >>> try:
      ...     _ = parse_git_branch_ref("refs/heads/topic/invalid")
      ... except InvalidRef as exc:
      ...     print(exc.args[0])
      ... else:
      ...     print("Expected InvalidRef exception not raised")
      refs/heads/topic/invalid
    """
    git_ref_prefix = 'refs/heads/'
    if not ref.startswith(git_ref_prefix):
        return None
    git_branch = ref[len(git_ref_prefix):]

    topic_prefix = 'topic/'
    if git_branch.startswith(topic_prefix):
        res = tuple(git_branch.split('/', 1)[1].rsplit('/', 1))
        if len(res) != 2:
            raise InvalidRef(ref)
        return res

    named_branch_prefix = 'branch/'
    if git_branch.startswith(named_branch_prefix):
        return git_branch[len(named_branch_prefix):], None


class GitRefChange(object):
    """Represent a change to be performed in a target Git repo.

    Public attributes:

    - :attr:`ref`: Git ref name
    - :attr:`before`, :attr:`after`: Git SHAs

    These will be complemented with a system of options, e.g., to specify that
    a topic change actually comes with publication, leading to a deferred
    removal of the corresponding Git branch once all appropriate treatments are
    done, whether this removal is performed from here or by GitLab.
    """

    def __init__(self, ref, before, after):
        self.ref = ref
        self.before = before
        self.after = after


class HeptapodGitHandler(GitHandler):

    def __init__(self, *args, **kwargs):
        super(HeptapodGitHandler, self).__init__(*args, **kwargs)

        main_repo = hg.sharedreposource(self.repo)
        if main_repo is None:
            main_repo = self.repo

        self.gitdir = re.sub(r'\.hg$', '', main_repo.root) + '.git'
        self._gl_hooks = {}
        self.unfiltered_repo = self.repo.unfiltered()

    def heptapod_gate_bookmarks(self, repo, allow, changes):
        """First handling of bookmark changes (refuse or not), return deleted.

        :param repo: passed explicitely because filtering may differ from
                     :attr:`repo`.
        :return: iterable of deleted bookmarks
        """
        if not changes:
            return ()

        ui = repo.ui
        deleted = []
        ui.note("HeptapodGitHandler bookmark changes=%r" % changes)
        new_bookmarks = []

        for name, change in changes.items():
            if change[0] is None:
                new_bookmarks.append(name)
            elif change[1] is None:
                deleted.append(name)

        if new_bookmarks and not allow:
            raise error.Abort(_(
                "Creating bookmarks is forbidden by default in Heptapod "
                "(got these new ones: %r). "
                "See https://heptapod.net/pages/faq.html#bookmarks to "
                "learn why and how to partially lift "
                "that restriction" % new_bookmarks))
        for new_bm_name, (_ign, new_bm_node) in pycompat.iteritems(changes):
            new_bm_ctx = repo[new_bm_node]
            new_bm_topic = new_bm_ctx.topic()
            if new_bm_topic:
                raise error.Abort(_(
                    "Creating or updating bookmarks on topic "
                    "changesets is forbidden"),
                    hint="topic %r and bookmark %r for changeset %s" % (
                        new_bm_topic, new_bm_name, new_bm_ctx.hex()))
        return deleted

    def get_exportable(self):
        """Heptapod version, including named branches and topics.

        This rewraps :meth:`GitHandler.get_exportable` to add named branches
        and topics to the returned Git refs
        """
        git_refs = super(HeptapodGitHandler, self).get_exportable()
        logprefix = 'HeptapodGitHandler.get_exportable '
        repo = self.repo.filtered('served')
        ui = repo.ui

        # "exporting" the ZERO_SHA will mean by convention a request to prune
        # the corresponding heads -- only a request, we can't really decide
        # at this stage.
        # The value is a dict mapping refs to reasons (just strings)
        to_prune = git_refs[ZERO_SHA] = {}

        txn = repo.currenttransaction()
        allow_bookmarks = ui.configbool('experimental',
                                        'hg-git.bookmarks-on-named-branches')
        bm_changes = txn.changes.get('bookmarks') if txn is not None else None
        deleted_bms = self.heptapod_gate_bookmarks(
            repo, allow_bookmarks, bm_changes)

        to_prune.update((git_branch_ref(bm), 'deleted-bookmark')
                        for bm in deleted_bms)
        all_bookmarks = self.repo._bookmarks
        # currently, self_filter_for_bookmarks() only does some renaming,
        # and doesn't discard any, so this is actually just equivalent to
        # hgshas of all bookmarks, but that may change in future hg-git
        hgshas_with_bookmark_git_ref = {
            hex(all_bookmarks[bm])
            for _, bm in self._filter_for_bookmarks(all_bookmarks)}
        for branch, hg_nodes in repo.branchmap().iteritems():
            gb = self.git_branch_for_branchmap_branch(branch)

            if ui.configbool('experimental',
                             'hg-git.prune-newly-closed-branches', True):
                hg_nodes = [n for n in hg_nodes if not repo[n].closesbranch()]
                if not hg_nodes:
                    to_prune[git_branch_ref(gb)] = 'closed'
            hg_shas = {hex(n) for n in hg_nodes}

            # We ignore bookmarked changesets because:
            # - we don't want them in the 'wild' namespace
            # - no other Git ref would be relevant for them
            hg_shas.difference_update(hgshas_with_bookmark_git_ref)
            if not hg_shas:
                if hg_nodes and allow_bookmarks:
                    # after removal of bookmarks, but not before,
                    # there is no hg head on this named branch:
                    # schedule potential removal. We don't want to do
                    # this if bookmarks aren't explicitely allowed because
                    # this must be a side effect, potentially disturbing, of
                    # an implicit bookmark move
                    to_prune[git_branch_ref(gb)] = 'only-bookmarks'
                ui.note(logprefix,
                        "Branch %r has no visible"
                        "non-bookmarked head" % branch)
                continue

            if 1 < len(hg_shas):
                ui.note(logprefix, "Multiple heads for branch %r: %r" % (
                    branch, hg_shas))
                for hg_sha in hg_shas:
                    git_refs[hg_sha].heads.add(
                        git_branch_ref('wild/' + hg_sha))
                gca = self.multiple_heads_choose(hg_shas, branch)
                if gca is None:
                    # giving up in order to avoid confusing situations
                    continue
                gca_sha = self.repo[gca].hex()
                ui.note(logprefix,
                        "Chose %r out of multiple heads %r "
                        "for forwarding branch %r" % (
                            gca_sha, hg_shas, branch))
                hg_shas = [gca_sha]
            hg_sha = hg_shas.pop()
            gb = self.git_branch_for_branchmap_branch(branch)
            git_refs[hg_sha].heads.add(git_branch_ref(gb))
        return git_refs

    def published_topic_latest_hg_sha(self, topic, ctx, log_before_ctx=None):
        ui = self.repo.ui
        try:
            after_ctx = self.latest_topic_descendant(topic, ctx)
        except MultipleDescendants:
            msg = ("Found several descendants in topic %r of the "
                   "newly published %r. Can't have GitLab add them "
                   "to any related merge request. ") % (topic, ctx)
            ui.warn(msg)
            ui.status(msg)
            # since successor is public, chances to detect merge are good
            return ctx.hex()

        ui.note('HeptapodGitHandler.published_topic_latest_hg_sha',
                "updating published %r from %r to %r" % (
                    topic,
                    log_before_ctx if log_before_ctx is not None else ctx,
                    after_ctx))
        return after_ctx.hex()

    def analyse_vanished_topic(self, branch, topic, before_sha,
                               log_info):
        """Compute revision to send GitLab as new topic branch head.

        This method does not access the Git repository.

        :param before_sha: Mercurial SHA for the current Git head of the topic
                           GitLab branch. Can be ``None`` if the Git head is
                           actually unknown to Mercurial.
        :param log_info: dict of useful information for logs that we must
                         restrain not to use for other purposes in this method
                         (typically some Git context)
        :return: Mercurial SHA, or ``None`` to trigger pruning.
        """
        logprefix = 'HeptapodGitHandler.topic_new_hg_sha '
        ui = self.repo.ui
        initial_import = ui.configbool(b"heptapod", b"initial-import")
        try:
            # TODO case where before_sha is None. same error treatment?
            before_ctx = self.unfiltered_repo[before_sha]
        except error.RepoLookupError:
            ui.warn(logprefix, "Git {ref!r} "
                    "(gitsha={before_git_sha}, hgsha={before_sha}) not "
                    "found in the Mercurial repo (should be due to "
                    "some half-rollbacked previous transaction), pruning "
                    "as the topic does not seem to be visible anymore".format(
                        before_sha=before_sha, **log_info))
            return None

        if before_ctx.phase() == phases.public:
            return self.published_topic_latest_hg_sha(topic, before_ctx)

        try:
            succctx = self.latest_unique_successor(before_ctx)
        except error.Abort as exc:
            if initial_import:
                # we don't want to break an initial import because
                # of an exceptional phase divergence, let's keep it unchanged
                ui.warn(logprefix + exc.args[0])
                return before_sha
            else:
                raise

        if succctx is None:
            ui.note(logprefix,
                    "scheduling prune of {ref} "
                    "(obsolete, no successor)".format(**log_info))
            return None

        succ_phase = succctx.phase()
        if succ_phase == phases.public:
            # not using succctx.topic() here because it is empty for
            # public changesets
            if succctx.extra().get(extrakey) == topic and not initial_import:
                return self.published_topic_latest_hg_sha(
                    topic, succctx, log_before_ctx=before_ctx)

        elif succ_phase == phases.draft:
            # let's go over some reasons why there's no visible branch/topic
            # head and the former one is obsolete with a draft successor
            succ_brtop = (succctx.branch(), succctx.topic())
            before_brtop = (before_ctx.branch(), before_ctx.topic())
            if succ_brtop != before_brtop:
                ui.note(logprefix,
                        "pruning %r (hgsha {before}), as its successor {succ} "
                        "is on another branch or topic".format(
                            before=before_ctx.hex(),
                            succ=succctx.hex(),
                            **log_info))
                return None

        return succctx.hex()

    def generate_prune_changes(self, to_prune, existing):
        """Generate those pruning Git changes that really have to be done.

        :return: a `dict` mapping Git refs to the :class:`Changes`
                 instances that will prune them.

        This method does not use the Git repo, only the :meth:`map_hg_get`
        """
        changes = {}
        prune_previously_closed_branches = self.repo.ui.configbool(
            'experimental', 'hg-git.prune-previously-closed-branches')
        for ref, reason in pycompat.iteritems(to_prune):
            before_sha = existing.get(ref)
            if before_sha is None:
                continue
            if reason == 'closed' and not prune_previously_closed_branches:
                before_hg_sha = self.map_hg_get(before_sha)
                if before_hg_sha is not None:
                    try:
                        before_ctx = self.repo[before_hg_sha]
                    except error.RepoLookupError:
                        # we can't really know if the closing is new,
                        # but being unknown to Mercurial, it certainly has
                        # to be pruned
                        self.repo.ui.warn(
                            "Pruning closed branch %r, whose "
                            "latest Git commit %r corresponds to the unknown "
                            "%r hg sha" % (ref, before_sha, before_hg_sha))
                    else:
                        if before_ctx.closesbranch():
                            # it was already closed
                            continue
            changes[ref] = GitRefChange(ref, before_sha, ZERO_SHA)
        return changes

    def analyze_vanished_refs(self, existing, exportable):
        """Decide what to do of existing Git refs that aren't in exportable.

        Some will have to be pruned, some other (published topics) will
        not.

        :return: dict mapping refs to `GitRefChange` instance to apply
        """
        changes = {}
        exported_refs = {ref for heads_tags in exportable.values()
                         for ref in heads_tags}
        for ref, before_git_sha in pycompat.iteritems(existing):
            if ref in exported_refs:
                continue

            if ref.startswith('refs/heads/wild/'):
                changes[ref] = GitRefChange(ref, before_git_sha, ZERO_SHA)

            try:
                branch_topic = parse_git_branch_ref(ref)
            except InvalidRef:
                self.repo.ui.warn("Git mirror repo has a bogus branch ref %r "
                                  "that's not among the exportable ones. "
                                  "Ignoring it.")
                continue
            if branch_topic is not None and branch_topic[1]:
                branch, topic = branch_topic
                before_hg_sha = self.map_hg_get(before_git_sha)
                after_hg_sha = self.analyse_vanished_topic(
                    branch, topic, before_hg_sha,
                    log_info=dict(ref=ref, before_git_sha=before_git_sha),
                    )
                if after_hg_sha is None:
                    after_git_sha = ZERO_SHA
                else:
                    after_git_sha = self.map_git_get(after_hg_sha)
                    if after_git_sha is None:
                        self.repo.ui.warn(
                            "Analysis of topic %r for branch %r "
                            "that becomes invisible in this transaction "
                            "to report its latest change to GitLab "
                            "found Mercurial changeset %r that has no known "
                            "Git counterpart. Giving up on reporting "
                            "that topic/branch combination to GitLab." % (
                                topic, branch, after_hg_sha))
                        continue

                changes[ref] = GitRefChange(ref, before_git_sha, after_git_sha)
        return changes

    def compare_exportable(self, existing, exportable):
        """Analyse the exportable refs to produce Git changes

        :param exportable: a mapping from Git refs to Mercurial SHAs
        :param existing: a mapping of existing Git refs in the target repo
                         to Git SHAs
        :returns: a mapping from Git refs to :class:`GitRefChange` objects
        """
        # we're not writing HEAD but apparently GitLab does, with
        # the ref for its default branch, and that's the best detection
        # we have of that.
        default_branch_ref = self.git.refs.get_symrefs().get('HEAD')
        to_prune = exportable.pop(ZERO_SHA, {})
        to_prune.pop(default_branch_ref, None)
        changes = self.generate_prune_changes(to_prune, existing)

        changes.update(self.analyze_vanished_refs(existing, exportable))

        for hg_sha, refs in pycompat.iteritems(exportable):
            for ref in refs.heads:
                after_sha = self.map_git_get(hg_sha)
                before_sha = existing.get(ref, ZERO_SHA)
                if after_sha and after_sha != before_sha:
                    changes[ref] = GitRefChange(ref, before_sha, after_sha)
        return changes

    def gitlab_get_hook(self, name):
        hook = self._gl_hooks.get(name)
        if hook is None and gitlab is not None:
            hook = self._gl_hooks[name] = gitlab.Hook(name, self.repo)
        return hook

    def heptapod_notify_gitlab(self, hook_name, changes, allow_error=False):
        if not changes:
            return

        hook = self.gitlab_get_hook(hook_name)
        ui = self.repo.ui

        try:
            code, out, err = hook({ref: (ch.before, ch.after)
                                   for ref, ch in pycompat.iteritems(changes)})
        except Exception as exc:
            ui.error("GitLab update error (%r hook): %r\n%s" % (
                hook_name, exc, traceback.format_exc()))
            if allow_error:
                # that's an error in py-heptapod, could be a network failure
                # once we call the internal API directly, for instance
                return
            else:
                raise

        if code != 0:
            ui.error("Got code %r while sending GitLab %r hook details=%r" % (
                code, hook_name, err))
            quiet = ui.quiet
            ui.quiet = False
            ui.status("GitLab update error: %r. Because of this, some "
                      "changes won't be visible in the web interface" % err)
            ui.quiet = quiet
            if not allow_error:
                raise error.Abort(err.strip())

        # useful messages such as motd, merge requests links etc.
        quiet = ui.quiet
        ui.quiet = False
        ui.status(out)
        ui.quiet = quiet

    def heptapod_apply_changes(self, changes):
        self.heptapod_notify_gitlab('pre-receive', changes)
        git_refs = self.git.refs
        for change in pycompat.itervalues(changes):
            if change.after == ZERO_SHA:
                del git_refs[change.ref]
            else:
                git_refs[change.ref] = change.after

        def post_receive(txn):
            self.heptapod_notify_gitlab('post-receive', changes)

        txn = self.repo.currenttransaction()
        if txn is None:
            post_receive(None)
        else:
            txn.addpostclose('heptapod_git_sync', post_receive)

    def update_references(self):
        """Update or create refs in the target Git repo for Mercurial changes.

        This fires or schedules all appropriate notifications (GitLab hooks)
        """
        changes = self.compare_exportable(self.git.refs.as_dict(),
                                          self.get_exportable())
        self.heptapod_apply_changes(changes)

    def multiple_heads_choose(self, hg_shas, branchmap_branch):
        """Choose among multiple heads to forward the given branch

        The branch is given in branchmap format, i.e., `branch:topic` or
        `branch`.

        Return None if nothing satisfying has been found.

        Currently, we arbitrarily take the one with the highest revision
        number (hence the most recently added to *this* repository).
        The advantage is that the given branch will never disappear
        (confusing to users, and leading to some blocking situations,
        such as heptapod#101).

        This is consistent with what Mercurial does for label-adressing,
        and shouldn't be a problem for Heptapod, since we force-push to
        Git all the time
        """
        if self.repo.ui.configbool('unit-tests',
                                   'hg-git.multiple-heads-dont-choose'):
            return

        revs = self.repo.revs('max(%ls)', hg_shas)
        if len(revs) != 1:
            return None
        return revs.first()

    def git_branch_for_branchmap_branch(self, topbranch):
        """return Git branch name for hg branch names in branchmap()

        Does in particular the needed sanitizations to make it acceptable
        for a Git branch.

        :param topbranch: can be either a named branch name or follow the
                          branch:topic convention, as returned by branchmap()
        """
        topbranch = topbranch.replace(' ', '_')
        if ':' in topbranch:
            branch, topic = topbranch.split(':', 1)
            if '/' in topic:
                msg = "Invalid character '/' in topic name %r. " % topic
                if self.ui.configbool('experimental',
                                      'hg-git.accept-slash-in-topic-name'):
                    msg += ("Replacing with '-'. Rename before publishing or "
                            "you'll get serious problems.")
                    topic = topic.replace('/', '-')
                    self.ui.status(msg)
                    self.ui.warn(msg)
                else:
                    self.ui.status(msg)
                    raise error.Abort(msg)

            return '/'.join(('topic', branch, topic))
        return 'branch/' + topbranch

    def latest_topic_descendant(self, topic, ctx):
        """Return the latest public descendent of ctx in a given topic.

        Although this is not meaningful in regular Mercurial usage,
        it's necessary because we need GitLab to understand what happened to
        a Merge Request on a published topic, and that's not possible if
        its branch vanished.

        This checks that there is one public head of the topic.
        Otherwise the push should be refused as inconsistend.

        The changeset of ctx is assumed *not* to be filtered (aka, obsolete)
        (all current callers already have obsolescence information around) and
        to belong to the topic. Raises Python standard LookupError otherwise.
        """
        revs = self.repo.revs("heads(extra(topic, %s) and descendants(%d))",
                              topic, ctx.rev())
        if len(revs) > 1:
            raise MultipleDescendants(topic, ctx)
        rev = revs.first()
        if rev is None:
            raise LookupError(
                "Can't find public descendants of %r in topic %r" % (
                    ctx.hex(), topic))
        return self.repo[rev]

    def latest_unique_successor(self, ctx):
        """Return the latest of unique set of successors of a changeset.

        The changeset is given by its context, and a context is also returned,
        or `None` if there is no successor.

        `Abort` gets raised if there are several sets of successors.
        """
        successorssets = obsutil.successorssets(self.repo,
                                                ctx.node())
        if not successorssets:
            return None
        if len(successorssets) > 1:
            # There is more than one set of successors, so we have
            # a divergence, and we cannot handle it automatically
            raise error.Abort(("Changeset %r evolved into a "
                               "divergent state") % ctx.hex())

        # Single successor set: it can be one or many (split)
        # In all cases, we can take the last one.
        return self.repo[successorssets[0][-1]]
