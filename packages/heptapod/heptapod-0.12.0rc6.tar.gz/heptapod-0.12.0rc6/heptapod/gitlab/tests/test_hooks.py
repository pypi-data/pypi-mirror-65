# Copyright 2019-2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import pytest
from heptapod.testhelpers import (
    LocalRepoWrapper,
    )
from .. import (
    git_hook_format_changes,
    Hook,
    )

ZERO_SHA = "0" * 20


def test_git_hook_format_changes():
    changes = {'branch/newbr': (ZERO_SHA, "beef1234dead" + "a" * 8),
               'topic/default/zz': ("23cafe45" + "0" * 12, "1234" + "b" * 16),
               }
    assert set(git_hook_format_changes(changes).split('\n')) == {
        '00000000000000000000 beef1234deadaaaaaaaa branch/newbr',
        '23cafe45000000000000 1234bbbbbbbbbbbbbbbb topic/default/zz'
    }


def make_repo(base_dir, name):
    wrapper = LocalRepoWrapper.init(
        base_dir.join(name),
        config=dict(heptapod={'gitlab-shell': str(base_dir)}),
        )
    # by default, ui.environ IS os.environ (shared) but that isn't true
    # in WSGI contexts. In that case, it is a plain dict, the WSGI environment
    # indeed. For these tests, we need them to be independent.
    wrapper.repo.ui.environ = {}
    return wrapper


def test_hook(tmpdir):
    wrapper = make_repo(tmpdir, 'proj.hg')
    repo = wrapper.repo
    hook = Hook('post-something', repo)

    repo.ui.environ.update(
        HEPTAPOD_USERINFO_ID='23',
        HEPTAPOD_PROJECT_ID='1024',
    )

    assert str(hook) == "GitLab 'post-something' hook wrapper"
    env = hook.environ()

    assert env.get('HG_GIT_SYNC') == 'yes'
    assert env.get('GL_ID') == 'user-23'
    assert env.get('GL_REPOSITORY') == 'project-1024'

    # we didn't pollute original environment
    assert 'GL_ID' not in repo.ui.environ

    # calling with empty changes
    assert hook(()) == (0, '', '')

    # now with an executable
    # we need a pseudo Git repo
    tmpdir.join('proj.git').ensure(dir=True)

    hook_bin = tmpdir.ensure('hooks', dir=True).join('post-something')
    hook_bin.write('\n'.join((
        "#!/usr/bin/env python",
        "import sys",
        "sys.stderr.write('stderr of the post something hook')",
        "for line in sys.stdin.readlines():",
        "    sys.stdout.write(line)",
        "sys.exit(3)",
    )))
    hook_bin.chmod(0o700)
    changes = {'branch/newbr': (ZERO_SHA, "beef1234dead" + "a" * 8),
               'topic/default/zz': ("23cafe45" + "0" * 12, "1234" + "b" * 16),
               }

    code, out, err = hook(changes)
    assert code, err == (3, 'stderr of the post something hoko')
    assert set(out.splitlines()) == {
        '00000000000000000000 beef1234deadaaaaaaaa branch/newbr',
        '23cafe45000000000000 1234bbbbbbbbbbbbbbbb topic/default/zz'
    }


def test_missing_gitlab_shell(tmpdir):
    repo = LocalRepoWrapper.init(tmpdir).repo
    with pytest.raises(RuntimeError) as exc_info:
        Hook('post-something', repo)
    assert "Path to GitLab Shell" in exc_info.value.args[0]


def test_hook_missing_user(tmpdir):
    wrapper = make_repo(tmpdir, 'proj2.hg')
    repo = wrapper.repo
    hook = Hook('post-something', repo)

    repo.ui.environ['HEPTAPOD_PROJECT_ID'] = '1024'
    with pytest.raises(ValueError) as exc_info:
        hook.environ()
    assert 'User id' in exc_info.value.args[0]

    # and that gets catched, does not break the process
    code, out, err = hook(dict(master=(0, 1)))
    assert code != 0


def test_hook_missing_project(tmpdir):
    wrapper = make_repo(tmpdir, 'proj2.hg')
    repo = wrapper.repo
    hook = Hook('post-something', repo)

    repo.ui.environ['HEPTAPOD_USERINFO_ID'] = '3'
    with pytest.raises(ValueError) as exc_info:
        hook.environ()
    assert 'Project id' in exc_info.value.args[0]

    # and that gets catched, does not break the process
    code, out, err = hook(dict(master=(0, 1)))
    assert code != 0


def test_hook_skip(tmpdir):
    wrapper = make_repo(tmpdir, 'proj2.hg')
    repo = wrapper.repo
    repo.ui.environ['HEPTAPOD_SKIP_GITLAB_HOOK'] = 'pre-rcv'
    hook = Hook('pre-rcv', repo)
    assert hook(dict(master=(0, 1))) == (0, '', '')


def test_hook_skip_all(tmpdir):
    wrapper = make_repo(tmpdir, 'proj2.hg')
    repo = wrapper.repo
    repo.ui.environ['HEPTAPOD_SKIP_ALL_GITLAB_HOOKS'] = 'no'
    hook = Hook('pre-rcv', repo)
    # it's been called and failed because of lack of User id
    assert hook(dict(master=(0, 1)))[0] == 1

    repo.ui.environ['HEPTAPOD_SKIP_ALL_GITLAB_HOOKS'] = 'yes'
    hook = Hook('pre-rcv', repo)
    assert hook(dict(master=(0, 1))) == (0, '', '')
