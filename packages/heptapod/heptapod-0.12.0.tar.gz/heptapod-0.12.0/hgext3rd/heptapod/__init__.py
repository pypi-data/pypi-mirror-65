# Copyright 2019 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
"""
Server side Heptapod extension.

This extension should enclose all Mercurial modifications and commands
needed for Heptapod server operations.
"""
from mercurial.i18n import _
from mercurial import (
    cmdutil,
    error,
    exthelper,
    extensions,
    registrar,
    scmutil,
    ui as uimod,
    util,
)

from . import (
    topic as topicmod,
    git,
)

eh = exthelper.exthelper()

if util.safehasattr(registrar, 'configitem'):

    configtable = {}
    configitem = registrar.configitem(configtable)
    configitem(b'heptapod', b'repositories-root')
    configitem(b'heptapod', b'gitlab-shell')
    configitem(b'heptapod', b'mirror-path')

    # The following items affect other config items recognized by the core
    # or by extensions. The default value should be inert, i.e., would not
    # change anything, in particular would not revert to Heptapod defaults
    # (as in `required.hgrc`) what local configuration or command-line options
    # say.
    configitem(b'heptapod', b'initial-import', False)
    configitem(b'heptapod', b'allow-multiple-heads')
    configitem(b'heptapod', b'allow-bookmarks')


cmdtable = {}
command = registrar.command(cmdtable)


def uipopulate(ui):
    if ui.configbool(b'heptapod', b'initial-import'):
        ui.note(b'hgext3rd.heptapod',
                b"setting config options for initial import")
        ui.setconfig(b'experimental',
                     b'single-head-per-branch', False)
        ui.setconfig(b'experimental',
                     b'topic.publish-bare-branch', False)
        ui.setconfig(b'experimental',
                     b'hg-git.bookmarks-on-named-branches', True)
        ui.setconfig(b'experimental', b'hg-git.accept-slash-in-topic-name',
                     True)
        ui.setconfig(b'hggit', b'heptapod.initial-import', True)

    if ui.configbool(b'heptapod', b'allow-multiple-heads'):
        ui.setconfig(b'experimental', b'single-head-per-branch', False)

    if ui.configbool(b'heptapod', b'allow-bookmarks'):
        ui.setconfig(b'experimental', b'single-head-per-branch', False)
        ui.setconfig(b'experimental',
                     b'hg-git.bookmarks-on-named-branches', True)

    auto_publish = ui.config(b'heptapod', b'auto-publish')
    if auto_publish is not None:
        auto_publish = auto_publish.lower()
    if auto_publish == b'nothing':
        ui.setconfig(b'experimental', b'topic.publish-bare-branch', False)
    elif auto_publish == b'all':
        ui.setconfig(b'phases', b'publish', True)


@command(
    "pull-force-topic",
    [('f', 'force', None, _('run even when remote repository is unrelated')),
     ('r', 'rev', [], _('a remote changeset intended to be imported'),
      _('REV')),
     ] + cmdutil.remoteopts,
    _('[-r] [-f] TARGET_TOPIC')
)
def pull_force_topic(ui, repo, topic, source="default",
                     force=False, **opts):
    """Pull changesets from remote, forcing them to drafts with given topic.

    This is intended to import pull requests from an external system, such
    as Bitbucket. In many case, the changesets to import would have been
    made in a private fork, and could be public, most commonly shadowing the
    default branch.

    TARGET_TOPIC is the topic to set on the pulled changesets
    """
    pull_rev = opts.get('rev')
    ui.status("Pulling%s from %r, forcing new changesets to drafts with "
              "topic %r\n" % ('' if pull_rev is None else ' %r' % pull_rev,
                              source, topic))
    topic = topic.strip()
    if not topic:
        raise error.Abort(
            _("topic name cannot consist entirely of whitespace"))
    scmutil.checknewlabel(repo, topic, 'topic')
    return topicmod.pull_force(ui, repo, source, pull_rev, topic,
                               force=force, **opts)


@command('gitlab-mirror')
def gitlab_mirror(ui, repo):
    """Export changesets as Git commits in the GitLab repository."""
    git.HeptapodGitHandler(repo, repo.ui).export_commits()


def runsystem(orig, ui, cmd, environ, cwd, out):
    heptapod_env = {k: v for k, v in ui.environ.items()
                    if k.startswith('HEPTAPOD_')}
    if environ is None:
        environ = heptapod_env
    else:
        heptapod_env.update(environ)
    return orig(ui, cmd, environ=heptapod_env, cwd=cwd, out=out)


extensions.wrapfunction(uimod.ui, '_runsystem', runsystem)
