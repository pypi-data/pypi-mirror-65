# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Integration tests for the Git subsystem

In this case, "integration" means that we're testing the main methods,
using true Git repos, and the whole Hook logic. We may also need to create
complex transactions, with several commits, rebases, phase changes etc.
"""
from __future__ import absolute_import

from dulwich.protocol import ZERO_SHA
import pytest
import subprocess

from heptapod import gitlab
from heptapod.testhelpers import (
    LocalRepoWrapper,
    )
from mercurial import (
    error,
)
from ...git import (
    GitRefChange,
    HeptapodGitHandler,
)
from ..utils import common_config


def recording_hook(records, action=None):

    class Hook(object):
        def __init__(self, name, repo):
            self.name = name
            self.repo = repo

        def __call__(self, changes):
            records.append((self.name, changes))
            if action is not None:
                return action(self.name, changes)
            else:
                return 0, "hook %r ok" % self.name, 'no error'

    return Hook


def extract_git_branch_titles(branches):
    return {ref: info['title'] for ref, info in branches.items()}


class GitRepo(object):

    def __init__(self, path):
        self.path = path

    @classmethod
    def init(cls, path):
        subprocess.call(('git', 'init', '--bare', str(path)))
        return cls(path)

    def branch_titles(self):
        return extract_git_branch_titles(self.branches())

    def branches(self):
        out = subprocess.check_output(('git', 'branch', '-v', '--no-abbrev'),
                                      cwd=str(self.path))
        split_lines = (l.lstrip('*').strip().split(None, 2)
                       for l in out.splitlines())
        return {sp[0]: dict(sha=sp[1], title=sp[2]) for sp in split_lines}

    def tags(self):
        out = subprocess.check_output(('git', 'tag'), cwd=str(self.path))
        return set(l.strip() for l in out.splitlines())

    def commit_hash_title(self, revspec):
        out = subprocess.check_output(
            ('git', 'log', '-n1',  revspec, r'--pretty=format:%H|%s'),
            cwd=str(self.path))
        return out.strip().split('|')

    def set_symref(self, name, target_ref):
        self.path.join(name).write('ref: %s\n' % target_ref)


def make_main_repo(path):
    """Make repo with 2 public revs; return wrapper, ctx of rev 0

    The returned ctx is for the first changeset because we'll use it as
    a branching point, hence more often than the second.
    """
    config = common_config()
    config['extensions']['hggit'] = ''
    config['phases'] = dict(publish=False)

    wrapper = LocalRepoWrapper.init(path, config=config)
    ctx = wrapper.write_commit('foo', content='foo0', message="default0",
                               return_ctx=True)
    wrapper.write_commit('foo', content='foo1', message="default1")
    wrapper.set_phase('public', ['.'])
    return wrapper, ctx


def set_allow_bookmarks(repo_wrapper, value):
    repo_wrapper.repo.ui.setconfig(
        'experimental', 'hg-git.bookmarks-on-named-branches', value)


def set_prune_closed_branches(repo_wrapper, value):
    repo_wrapper.repo.ui.setconfig(
        'experimental', 'hg-git.prune-newly-closed-branches', value)


def activate_mirror(repo_wrapper):
    """Activate the mirrorring hook for given repo.

    Using the hook is a simple way to get in-transaction, while still within
    a repo fully controlled by these tests (configuration, notably).
    """
    repo_wrapper.repo.ui.setconfig(
        'hooks', 'pretxnclose.testcase',
        'python:heptapod.hooks.gitlab_mirror.mirror')


def test_basic(tmpdir, monkeypatch):
    notifs = []
    monkeypatch.setattr(gitlab, 'Hook', recording_hook(notifs))
    repo_path = tmpdir.join('repo.hg')
    repo, base_ctx = make_main_repo(repo_path)
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    repo.command('gitlab-mirror')

    assert git_repo.branch_titles() == {'branch/default': 'default1'}
    sha = git_repo.branches()['branch/default']['sha']
    assert notifs == [
        ('pre-receive', {'refs/heads/branch/default': (ZERO_SHA, sha)}),
        ('post-receive', {'refs/heads/branch/default': (ZERO_SHA, sha)}),
    ]


def test_tags(tmpdir, monkeypatch):
    notifs = []
    monkeypatch.setattr(gitlab, 'Hook', recording_hook(notifs))
    repo_path = tmpdir.join('repo.hg')
    repo, base_ctx = make_main_repo(repo_path)
    git_repo = GitRepo.init(tmpdir.join('repo.git'))

    # Creation
    repo.command('tag', 'v1.2.3', rev=base_ctx.hex())
    repo.command('gitlab-mirror')

    branch_titles = git_repo.branch_titles()
    assert len(branch_titles) == 1
    assert 'v1.2.3' in branch_titles['branch/default']
    assert git_repo.tags() == {'v1.2.3', }
    assert git_repo.commit_hash_title('v1.2.3')[1] == 'default0'

    # Modification
    repo.command('tag', 'v1.2.3', rev='1', force=True)
    repo.command('gitlab-mirror')

    assert git_repo.tags() == {'v1.2.3', }
    assert git_repo.commit_hash_title('v1.2.3')[1] == 'default1'

    # Removal not supported in Heptapod 0.8. TODO later


def test_share(tmpdir, monkeypatch):
    notifs = []
    monkeypatch.setattr(gitlab, 'Hook', recording_hook(notifs))
    main_path = tmpdir.join('main.hg')
    main_wrapper, base_ctx = make_main_repo(main_path)
    git_repo = GitRepo.init(tmpdir.join('main.git'))

    # let's start with some commits in the Git repo
    main_wrapper.command('gitlab-mirror')
    assert git_repo.branch_titles() == {'branch/default': 'default1'}

    # now let's make a share
    dest_wrapper = main_wrapper.share(tmpdir.join('share.hg'))
    dest_wrapper.write_commit('bar', message='other0',
                              branch='other', parent=base_ctx.node())
    dest_wrapper.command('gitlab-mirror')
    assert git_repo.branch_titles() == {'branch/default': 'default1',
                                        'branch/other': 'other0'}


def test_bookmarks_prune(tmpdir, monkeypatch):
    notifs = []
    monkeypatch.setattr(gitlab, 'Hook', recording_hook(notifs))
    server_path = tmpdir.join('repo.hg')
    server, base_ctx = make_main_repo(server_path)
    server.command('bookmark', 'zebook', rev=base_ctx.hex())
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    # not being in a transaction accepts the bookmark immediately
    server.command('gitlab-mirror')
    assert git_repo.branch_titles() == {
        'branch/default': 'default1',
        'zebook': 'default0'
    }

    activate_mirror(server)
    server.command('bookmark', 'zebook', delete=True)

    assert server.repo.nodebookmarks(base_ctx.node()) == []
    assert git_repo.branch_titles() == {
        'branch/default': 'default1',
    }


def test_bookmarks_mask_branch_prune(tmpdir, monkeypatch):
    notifs = []
    monkeypatch.setattr(gitlab, 'Hook', recording_hook(notifs))
    server_path = tmpdir.join('repo.hg')
    server, base_ctx = make_main_repo(server_path)
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    server.command('gitlab-mirror')
    # just checking our assumptions
    assert git_repo.branch_titles() == {'branch/default': 'default1'}

    activate_mirror(server)
    set_allow_bookmarks(server, True)
    head = server.repo['tip']
    server.command('bookmark', 'zebook', rev=head.hex())
    assert git_repo.branch_titles() == {
        'zebook': 'default1'
    }

    server.command('bookmark', 'zebook', delete=True)

    assert server.repo.nodebookmarks(head.node()) == []
    assert git_repo.branch_titles() == {
        'branch/default': 'default1',
    }


def test_closed_branch(tmpdir, monkeypatch):
    notifs = []
    monkeypatch.setattr(gitlab, 'Hook', recording_hook(notifs))
    wrapper, base_ctx = make_main_repo(tmpdir.join('repo.hg'))
    wrapper.write_commit('foo', message="other0",
                         branch='other',
                         parent=base_ctx.node(),
                         return_ctx=True)
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    wrapper.command('gitlab-mirror')
    assert git_repo.branch_titles() == {'branch/default': 'default1',
                                        'branch/other': 'other0'}
    set_prune_closed_branches(wrapper, True)
    wrapper.command('commit', message="closing other", close_branch=True)
    wrapper.command('gitlab-mirror')
    assert git_repo.branch_titles() == {'branch/default': 'default1'}


def test_previously_closed_branch_not_pruned(tmpdir, monkeypatch):
    notifs = []
    monkeypatch.setattr(gitlab, 'Hook', recording_hook(notifs))
    wrapper, base_ctx = make_main_repo(tmpdir.join('repo.hg'))
    wrapper.write_commit('foo', message="other0",
                         branch='other',
                         parent=base_ctx.node(),
                         return_ctx=True)
    git_repo = GitRepo.init(tmpdir.join('repo.git'))

    # let's prepare a closed branch that hasn't been prune
    set_prune_closed_branches(wrapper, False)
    wrapper.command('commit', message="closing other", close_branch=True)
    wrapper.command('gitlab-mirror')
    assert git_repo.branch_titles() == {'branch/default': 'default1',
                                        'branch/other': 'closing other'}

    # subsequent calls won't prune it
    set_prune_closed_branches(wrapper, True)
    wrapper.repo.ui.setconfig(
        'experimental', 'hg-git.prune-previously-closed-branches', False)
    wrapper.command('gitlab-mirror')

    assert git_repo.branch_titles()['branch/other'] == 'closing other'


def test_closed_branch_not_in_git(tmpdir, monkeypatch):
    notifs = []
    monkeypatch.setattr(gitlab, 'Hook', recording_hook(notifs))
    wrapper, base_ctx = make_main_repo(tmpdir.join('repo.hg'))
    wrapper.write_commit('foo', message="other0",
                         branch='other',
                         parent=base_ctx.node(),
                         return_ctx=True)
    git_repo = GitRepo.init(tmpdir.join('repo.git'))

    # the `other` branch being mirrored as already closed, will trigger
    # a prune request that should be ignored in order not to fail
    wrapper.command('commit', message="closing other", close_branch=True)
    wrapper.command('gitlab-mirror')
    assert git_repo.branch_titles() == {'branch/default': 'default1'}


def test_closed_default_branch(tmpdir, monkeypatch):
    notifs = []
    monkeypatch.setattr(gitlab, 'Hook', recording_hook(notifs))
    wrapper, base_ctx = make_main_repo(tmpdir.join('repo.hg'))
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    wrapper.command('gitlab-mirror')
    assert git_repo.branch_titles() == {'branch/default': 'default1'}
    git_repo.set_symref('HEAD', 'refs/heads/branch/default')

    set_prune_closed_branches(wrapper, True)
    wrapper.command('commit', message="closing default!", close_branch=True)
    wrapper.command('gitlab-mirror')
    assert git_repo.branch_titles() == {'branch/default': 'default1'}


def test_multiple_heads_merge(tmpdir, monkeypatch):
    notifs = []
    monkeypatch.setattr(gitlab, 'Hook', recording_hook(notifs))
    wrapper, base_ctx = make_main_repo(tmpdir.join('repo.hg'))
    first = wrapper.repo['tip']
    second = wrapper.write_commit('bar', message="second head",
                                  branch='default',
                                  parent=base_ctx.node(),
                                  return_ctx=True)
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    wrapper.command('gitlab-mirror')
    assert git_repo.branch_titles() == {
        'wild/' + first.hex(): 'default1',
        'wild/' + second.hex(): 'second head',
        # the most recently added revision always wins
        'branch/default': 'second head',
    }
    wrapper.command('merge')
    wrapper.command('commit', message='merging heads')
    wrapper.command('gitlab-mirror')
    assert git_repo.branch_titles() == {'branch/default': 'merging heads'}


def test_multiple_heads_cannot_choose(tmpdir, monkeypatch):
    notifs = []
    monkeypatch.setattr(gitlab, 'Hook', recording_hook(notifs))
    wrapper, base_ctx = make_main_repo(tmpdir.join('repo.hg'))
    first = wrapper.repo['tip']
    second = wrapper.write_commit('bar', message="second head",
                                  branch='default',
                                  parent=base_ctx.node(),
                                  return_ctx=True)
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    wrapper.repo.ui.setconfig('unit-tests',
                              'hg-git.multiple-heads-dont-choose', True)
    wrapper.command('gitlab-mirror')

    # not being able to choose, we don't have the GitLab branch for 'default'
    assert git_repo.branch_titles() == {
        'wild/' + first.hex(): 'default1',
        'wild/' + second.hex(): 'second head',
    }

    # for the sake of it, let's check that a merge gets back to normal
    wrapper.command('merge')
    wrapper.command('commit', message='merging heads')
    wrapper.command('gitlab-mirror')
    assert git_repo.branch_titles() == {'branch/default': 'merging heads'}


def test_push_multiple_heads_switch_branch(tmpdir, monkeypatch):
    notifs = []
    monkeypatch.setattr(gitlab, 'Hook', recording_hook(notifs))
    wrapper, base_ctx = make_main_repo(tmpdir.join('repo.hg'))
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    # second head on default branch (easy to merge for later test)
    wrapper.write_commit('bar', message="default head 2",
                         parent=base_ctx.node())
    default_heads_titles = {'default1', 'default head 2'}

    wrapper.command('gitlab-mirror')

    branch_titles = git_repo.branch_titles()
    assert set(branch_titles.values()) == default_heads_titles
    assert len(branch_titles) == 3

    wrapper.write_commit('foo', message="other", branch='other')
    wrapper.command('gitlab-mirror')
    branch_titles = git_repo.branch_titles()
    assert set(branch_titles.values()) == default_heads_titles | {'other', }
    assert len(branch_titles) == 4

    # now let's add a topic on top of one of those wild 'default' heads
    wrapper.write_commit('foo', message="on topic",
                         topic='zetop',
                         parent=base_ctx.node())

    wrapper.command('gitlab-mirror')
    branch_titles = git_repo.branch_titles()
    assert set(b for b in branch_titles if not b.startswith('wild/')) == {
        'branch/default', 'branch/other', 'topic/default/zetop'}

    assert set(title
               for name, title in branch_titles.items()
               if name.startswith('wild/')) == default_heads_titles
    assert branch_titles['branch/default'] in default_heads_titles
    assert branch_titles['branch/other'] == 'other'
    assert branch_titles['topic/default/zetop'] == 'on topic'


def test_topic_pruned(tmpdir, monkeypatch):
    notifs = []
    monkeypatch.setattr(gitlab, 'Hook', recording_hook(notifs))
    wrapper, _ = make_main_repo(tmpdir.join('repo.hg'))
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    wrapper.write_commit('foo', message='in topic', topic='zzetop')
    wrapper.command('gitlab-mirror')
    del notifs[:]

    branches_before = git_repo.branches()
    assert extract_git_branch_titles(branches_before) == {
        'branch/default': 'default1',
        'topic/default/zzetop': 'in topic'}

    wrapper.prune('zzetop')
    wrapper.command('gitlab-mirror')

    topic_change = {'refs/heads/topic/default/zzetop': (
        branches_before['topic/default/zzetop']['sha'],
        ZERO_SHA,
    )}

    assert git_repo.branch_titles() == {
        'branch/default': 'default1',
    }
    assert notifs == [('pre-receive', topic_change),
                      ('post-receive', topic_change)]


def test_topic_amended(tmpdir, monkeypatch):
    notifs = []
    monkeypatch.setattr(gitlab, 'Hook', recording_hook(notifs))
    repo_path = tmpdir.join('repo.hg')
    wrapper, _ = make_main_repo(repo_path)
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    wrapper.write_commit('foo', message='in topic', topic='zzetop')
    wrapper.command('gitlab-mirror')
    del notifs[:]

    branches_before = git_repo.branches()
    assert extract_git_branch_titles(branches_before) == {
        'branch/default': 'default1',
        'topic/default/zzetop': 'in topic'}

    repo_path.join('foo').write('amend1')
    wrapper.command('amend', message='amend1')

    wrapper.command('gitlab-mirror')

    branches = git_repo.branches()
    assert extract_git_branch_titles(branches) == {
        'branch/default': 'default1',
        'topic/default/zzetop': 'amend1',
    }

    topic_change = {'refs/heads/topic/default/zzetop': (
        branches_before['topic/default/zzetop']['sha'],
        branches['topic/default/zzetop']['sha'],
    )}

    assert notifs == [('pre-receive', topic_change),
                      ('post-receive', topic_change)]


def test_topic_ff_publish(tmpdir, monkeypatch):
    notifs = []
    monkeypatch.setattr(gitlab, 'Hook', recording_hook(notifs))
    wrapper, _ = make_main_repo(tmpdir.join('repo.hg'))
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    wrapper.command('topics', 'zzetop')
    wrapper.write_commit('foo', message='in ff topic')
    wrapper.command('gitlab-mirror')
    del notifs[:]

    branches_before = git_repo.branches()
    assert extract_git_branch_titles(branches_before) == {
        'branch/default': 'default1',
        'topic/default/zzetop': 'in ff topic'}

    wrapper.set_phase('public', ['zzetop'])
    wrapper.command('gitlab-mirror')

    assert git_repo.branch_titles() == {
        'branch/default': 'in ff topic',
        'topic/default/zzetop': 'in ff topic',
    }

    # we're sending notifications for the topic GitLab branch,
    # with unchanged hash, hoping that's enough to trigger assessment of MR
    # from source branch on the GitLab side
    changes = {
        'refs/heads/branch/default': (
            branches_before['branch/default']['sha'],
            branches_before['topic/default/zzetop']['sha'],
        ),
        'refs/heads/topic/default/zzetop': (
            branches_before['topic/default/zzetop']['sha'],
            branches_before['topic/default/zzetop']['sha'],
        )
    }

    assert notifs == [('pre-receive', changes),
                      ('post-receive', changes)]


def test_topic_rebase_publish(tmpdir, monkeypatch):
    notifs = []
    monkeypatch.setattr(gitlab, 'Hook', recording_hook(notifs))
    wrapper, _ = make_main_repo(tmpdir.join('repo.hg'))
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    wrapper.write_commit('zz', message='in topic', topic='zzetop')
    wrapper.command('gitlab-mirror')
    del notifs[:]

    branches_before = git_repo.branches()
    assert extract_git_branch_titles(branches_before) == {
        'branch/default': 'default1',
        'topic/default/zzetop': 'in topic'}

    wrapper.command('rebase', base='zzetop')
    wrapper.set_phase('public', ['zzetop'])
    wrapper.command('gitlab-mirror')

    branches_after = git_repo.branches()
    assert extract_git_branch_titles(branches_after) == {
        'branch/default': 'in topic',
        'topic/default/zzetop': 'in topic'}

    changes = {
        'refs/heads/branch/default': (
            branches_before['branch/default']['sha'],
            branches_after['branch/default']['sha']),
        'refs/heads/topic/default/zzetop': (
            branches_before['topic/default/zzetop']['sha'],
            branches_after['branch/default']['sha']),
    }
    assert notifs == [('pre-receive', changes),
                      ('post-receive', changes)]


def test_topic_add_rebase_publish(tmpdir, monkeypatch):
    notifs = []
    monkeypatch.setattr(gitlab, 'Hook', recording_hook(notifs))
    wrapper, base_ctx = make_main_repo(tmpdir.join('repo.hg'))
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    wrapper.write_commit('zz', message='in topic',
                         parent=base_ctx.node(), topic='zzetop')
    wrapper.command('gitlab-mirror')
    del notifs[:]

    branches_before = git_repo.branches()
    assert extract_git_branch_titles(branches_before) == {
        'branch/default': 'default1',
        'topic/default/zzetop': 'in topic'}

    wrapper.write_commit('zz', message='topic addition')
    wrapper.command('rebase', base='zzetop')
    wrapper.set_phase('public', ['zzetop'])
    wrapper.command('gitlab-mirror')

    branches_after = git_repo.branches()
    assert extract_git_branch_titles(branches_after) == {
        'branch/default': 'topic addition',
        'topic/default/zzetop': 'topic addition'}

    changes = {
        'refs/heads/branch/default': (
            branches_before['branch/default']['sha'],
            branches_after['branch/default']['sha']),
        'refs/heads/topic/default/zzetop': (
            branches_before['topic/default/zzetop']['sha'],
            branches_after['branch/default']['sha']),
    }
    assert notifs == [('pre-receive', changes),
                      ('post-receive', changes)]


def test_topic_branch_change(tmpdir, monkeypatch):
    notifs = []
    monkeypatch.setattr(gitlab, 'Hook', recording_hook(notifs))
    wrapper, base_ctx = make_main_repo(tmpdir.join('repo.hg'))
    git_repo = GitRepo.init(tmpdir.join('repo.git'))

    wrapper.write_commit('bar', message='other0',
                         parent=base_ctx.node(), branch='other')
    wrapper.write_commit('zz', message='in topic',
                         topic='zzetop')
    wrapper.command('gitlab-mirror')

    assert git_repo.branch_titles() == {
        'branch/default': 'default1',
        'branch/other': 'other0',
        'topic/other/zzetop': 'in topic'}

    wrapper.command('rebase', rev=['zzetop'], dest='default')
    wrapper.command('gitlab-mirror')
    assert git_repo.branch_titles() == {
        'branch/default': 'default1',
        'branch/other': 'other0',
        'topic/default/zzetop': 'in topic',
    }


def test_analyse_vanished_topic_not_in_git(tmpdir, monkeypatch):
    notifs = []
    monkeypatch.setattr(gitlab, 'Hook', recording_hook(notifs))
    wrapper, base_ctx = make_main_repo(tmpdir.join('repo.hg'))
    repo = wrapper.repo
    git_repo = GitRepo.init(tmpdir.join('repo.git'))

    wrapper.write_commit('zz', message='in topic', topic='zzetop')
    wrapper.command('gitlab-mirror')

    def return_unknown(handler, *a, **kw):
        handler.repo.test_patch_called = True
        return 'unknown-to-git'

    # let's make the published topic analysis return something unknown to Git
    monkeypatch.setattr(HeptapodGitHandler, 'analyse_vanished_topic',
                        return_unknown)

    wrapper.set_phase('public', ['zzetop'])
    # Calling export directly because through the hook, such
    # monkey patching often does not work.
    HeptapodGitHandler(repo, repo.ui).export_commits()

    # we didn't fail and have been conservative with the topic GitLab branch
    assert git_repo.branch_titles() == {
        'branch/default': 'in topic',
        'topic/default/zzetop': 'in topic'
    }

    # note that coverage would notice if the test harness didn't work
    assert wrapper.repo.test_patch_called


def test_heptapod_notify_gitlab(tmpdir, monkeypatch):
    wrapper = LocalRepoWrapper.init(tmpdir.join('repo'))
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)

    notifs = []

    def trigger_failures(name, changes):
        if 'exc' in changes:
            raise RuntimeError('trigger_failures: ' + name)
        if 'code_one' in changes:
            return 1, '', 'hook refusal'
        return 0, 'Consider a MR for %r' % name, ''

    monkeypatch.setattr(gitlab, 'Hook',
                        recording_hook(notifs, action=trigger_failures))

    # minimal valid change
    change = GitRefChange('master', 'before', 'after')
    handler.heptapod_notify_gitlab('some-hook', dict(master=change),
                                   allow_error=False)
    assert notifs == [('some-hook', {'master': ('before', 'after')})]
    del notifs[:]

    with pytest.raises(error.Abort) as exc_info:
        handler.heptapod_notify_gitlab('some-hook', dict(code_one=change),
                                       allow_error=False)
    assert "hook refusal" in exc_info.value.args[0]

    with pytest.raises(RuntimeError) as exc_info:
        handler.heptapod_notify_gitlab('some-hook', dict(exc=change),
                                       allow_error=False)
    assert "trigger_failures" in exc_info.value.args[0]

    # case where exception is triggered yet is accepted
    errors = []

    def record_ui_error(*args):
        errors.append(args)
    monkeypatch.setattr(handler.repo.ui, 'error', record_ui_error)
    handler.heptapod_notify_gitlab('some-hook', dict(exc=change),
                                   allow_error=True)
    assert errors[0][0].splitlines()[:2] == [
        "GitLab update error ('some-hook' hook): "
        "RuntimeError('trigger_failures: some-hook',)",
        "Traceback (most recent call last):"
    ]
