# Copyright 2019-2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from __future__ import absolute_import
import pytest
from mercurial import (
    error,
    phases,
)
from heptapod.testhelpers import (
    LocalRepoWrapper,
    )

from .utils import switch_user


def init_repo(basedir):
    return LocalRepoWrapper.init(
        basedir,
        config=dict(
            phases={'publish': 'no'},
            hooks={'pretxnclose.check_publish':
                   'python:heptapod.hooks.check_publish.check_publish'
                   },
            web={'allow-publish': 'maintainer',
                 'allow-push': '*',
                 },
        ))


def test_draft_publish(tmpdir):
    wrapper = init_repo(tmpdir)
    switch_user(wrapper, 'someone')
    ctx = wrapper.write_commit('foo', content='Foo', return_ctx=True)
    assert ctx.phase() == phases.draft

    with pytest.raises(error.Abort) as exc_info:
        wrapper.set_phase('public', [ctx.hex()])
    expected_msg = 'user "someone" is not authorised to publish changesets'
    assert expected_msg in exc_info.value.args[0]

    switch_user(wrapper, 'maintainer')
    wrapper.set_phase('public', [ctx.hex()])
    assert ctx.phase() == phases.public


def test_wrong_hook(tmpdir):
    wrapper = init_repo(tmpdir)
    ui = wrapper.repo.ui
    pretxn = 'pretxnclose.check_publish'
    hookdef = ui.config('hooks', pretxn)
    ui.setconfig('hooks', pretxn, '')
    ui.setconfig('hooks', 'precommit.check_publish', hookdef)
    # precommit because that one does not swallow exceptions other
    # than abort
    with pytest.raises(error.ProgrammingError) as exc_info:
        wrapper.write_commit('foo')

    assert 'precommit' in exc_info.value.args[0]
