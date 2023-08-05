# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Inner tests for the Git subsystem.

These wouldn't really qualify as unit tests, since they exert at least
Mercurial, but they are more unitary and disposable than those of
test_integration, testing the implementation details of the Git subsystem.
"""
from __future__ import absolute_import

from mercurial import (
    error,
)
import pytest

from heptapod.testhelpers import (
    LocalRepoWrapper,
    )
from ...git import (
    HeptapodGitHandler,
)
from ..utils import common_config


def test_heptapod_gate_bookmarks(tmpdir):
    wrapper = LocalRepoWrapper.init(tmpdir.join('repo'),
                                    config=common_config())
    ctx = wrapper.write_commit('foo', content='foo0', message="default0",
                               return_ctx=True)

    repo = wrapper.repo
    handler = HeptapodGitHandler(repo, repo.ui)
    gate = handler.heptapod_gate_bookmarks

    assert len(gate(repo, True, {})) == 0

    with pytest.raises(error.Abort) as exc_info:
        gate(repo, False, dict(book1=(None, '\x00\x01')))
    assert 'forbidden' in exc_info.value.args[0]
    assert 'book1' in exc_info.value.args[0]

    deleted = gate(repo, False, dict(book1=('\x00\x01', None)))
    assert list(deleted) == ['book1']

    deleted = gate(repo, True, dict(book1=('\x00\x01', None)))
    assert list(deleted) == ['book1']

    deleted = gate(repo, True, dict(book1=(None, ctx.node())))
    assert not deleted

    wrapper.command('topics', 'zetop')
    node = wrapper.write_commit('zz', message='topical')
    with pytest.raises(error.Abort) as exc_info:
        gate(repo, True, dict(book1=(None, node)))
    assert 'forbidden' in exc_info.value.args[0]
    assert 'topic' in exc_info.value.args[0]


def test_git_branch_for_branchmap_branch(tmpdir):
    wrapper = LocalRepoWrapper.init(tmpdir.join('repo'))
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    gb = handler.git_branch_for_branchmap_branch

    assert gb('default') == 'branch/default'
    assert gb('default:zztop') == 'topic/default/zztop'

    with pytest.raises(error.Abort) as exc_info:
        assert gb('default:zz/top')
    assert "Invalid character '/'" in exc_info.value.args[0]

    wrapper.repo.ui.setconfig('experimental',
                              'hg-git.accept-slash-in-topic-name', True)

    assert gb('default:zz/top') == 'topic/default/zz-top'


def test_multiple_heads_choose_corner_case(tmpdir):
    wrapper = LocalRepoWrapper.init(tmpdir.join('repo'))
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    assert handler.multiple_heads_choose((), 'branch name') is None


def test_notify_gitlab_empty_changes(tmpdir):
    wrapper = LocalRepoWrapper.init(tmpdir.join('repo'))
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    assert handler.heptapod_notify_gitlab('some-hook', {}) is None


def test_analyse_vanished_topic_lookup_error(tmpdir):
    wrapper = LocalRepoWrapper.init(tmpdir.join('repo'))
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    unknown_sha = '1234beef' * 5
    new_sha = handler.analyse_vanished_topic(
        'default', 'zetop', unknown_sha,
        log_info=dict(ref='refs/heads/topic/default/zetop',
                      before_git_sha='01234cafe'))
    assert new_sha is None


def test_analyse_vanished_bogus_topic(tmpdir):
    wrapper = LocalRepoWrapper.init(tmpdir.join('repo'))
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    assert handler.analyze_vanished_refs(
        {'refs/heads/topic/missing-branch-name': 'ca1234fe',
         'refs/heads/branch/default': 'will be completely ignored anyway'},
        {'refs/heads/branch/default': 'will be completely ignored anyway'},
    ) == {}


def test_analyse_vanished_topic_draft_succ_unknown_reason(tmpdir):
    wrapper = LocalRepoWrapper.init(tmpdir.join('repo'),
                                    config=common_config())
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    wrapper.write_commit('foo', message='foo0')
    ctx = wrapper.write_commit('foo', message='in topic', topic='zzetop',
                               return_ctx=True)

    # Normally, analyse_vanished_topic works under the assumption that
    # the topic is not visible anymore. Yet feeding a visible topic
    # is the only currently known way of triggering the safety return
    # of before_sha for unknown situations (that could also be a life saver
    # if a visible topic were passed by mistake)

    after_sha = handler.analyse_vanished_topic(
        'default', 'zzetop',
        ctx.hex(),
        log_info=dict(ref='refs/heads/topic/default/zetop',
                      before_git_sha='01234cafe'))

    assert after_sha == ctx.hex()


def prepare_topic_divergence(tmpdir, additional_config=None):
    config = common_config()
    config['experimental'] = {'evolution.allowdivergence': 'yes'}
    if additional_config is not None:
        config.update(additional_config)
    repo_path = tmpdir.join('repo')
    wrapper = LocalRepoWrapper.init(repo_path, config=config)

    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    wrapper.write_commit('foo', content='foo0', message="default0")
    ctx = wrapper.write_commit('foo', content='obs', message="to obsolete",
                               return_ctx=True)

    # create a content divergence
    repo_path.join('foo').write('amend1')
    wrapper.command('amend', message='amend1')

    wrapper.update(ctx.hex(), hidden=True)
    repo_path.join('foo').write('amend2')
    wrapper.command('amend', message='amend2')

    return wrapper, ctx, handler


def test_analyse_vanished_topic_divergence_initial_import(tmpdir):
    wrapper, ctx, handler = prepare_topic_divergence(
        tmpdir,
        additional_config=dict(heptapod={'initial-import': True}))

    handler.analyse_vanished_topic(
        'default', 'zetop',
        ctx.hex(),
        log_info=dict(ref='refs/heads/topic/default/zetop',
                      before_git_sha='01234cafe'))


def test_analyse_vanished_topic_divergence_not_initial_import(tmpdir):
    wrapper, ctx, handler = prepare_topic_divergence(tmpdir)

    with pytest.raises(error.Abort) as exc_info:
        handler.analyse_vanished_topic(
            'default', 'zetop',
            ctx.hex(),
            log_info=dict(ref='refs/heads/topic/default/zetop',
                          before_git_sha='01234cafe'))

    exc_msg = exc_info.value.args[0]
    assert ctx.hex() in exc_msg
    assert 'divergent' in exc_msg


def test_topic_published_multiple_heads(tmpdir):
    wrapper = LocalRepoWrapper.init(tmpdir.join('repo'),
                                    config=common_config())
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    wrapper.write_commit('foo', message='foo0')
    before_ctx = wrapper.write_commit('foo', message='in topic',
                                      topic='zzetop', return_ctx=True)

    # let's publish for the sake of consistency, but these inner tests
    # aren't based on the state of a Git repo anyway: previous state is
    # passed explicitely
    wrapper.set_phase('public', ['zzetop'])

    # let's add two public in topic descendants
    ctx1 = wrapper.write_commit('foo', message='this is wild 1',
                                parent=before_ctx.node(), topic='zzetop',
                                return_ctx=True)
    ctx2 = wrapper.write_commit('foo', message='this is wild 2',
                                parent=before_ctx.node(), topic='zzetop',
                                return_ctx=True)
    wrapper.set_phase('public', [ctx1.hex(), ctx2.hex()])

    after_hg_sha = handler.analyse_vanished_topic(
        'default', 'zzetop',
        before_ctx.hex(),
        log_info=dict(ref='refs/heads/topic/default/zzetop',
                      before_git_sha='01234cafe'))

    assert after_hg_sha == before_ctx.hex()


def test_latest_unique_successor_no_descendant(tmpdir):
    wrapper = LocalRepoWrapper.init(tmpdir.join('repo'),
                                    config=common_config())
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    ctx = wrapper.write_commit('foo', message='foo0', return_ctx=True)

    # this can happen only if ctx isn't itself in the wished topic
    # which our current callers always ensure.
    with pytest.raises(LookupError):
        handler.latest_topic_descendant('sometop', ctx)


def test_generate_prune_changes_existing_unknown(tmpdir):
    config = common_config()
    config['experimental'] = {'hg-git.prune-previously-closed-branches': 'no'}
    wrapper = LocalRepoWrapper.init(tmpdir.join('repo'), config=config)

    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)

    # let's have a git -> hg map that gives us an unknown hg sha.
    # it still has to be formally valid, though (hex, length 40)
    map_hg = {'1234': 'cafe' * 10}

    def map_hg_get(git_sha):
        return map_hg.get(git_sha)

    handler.map_hg_get = map_hg_get

    branch_ref = 'refs/heads/branch/previously-closed'
    existing = {branch_ref: '1234'}
    to_prune = {branch_ref: 'closed'}
    changes = handler.generate_prune_changes(to_prune, existing)

    assert branch_ref in changes
