# Copyright 2019-2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import os
import subprocess


def git_hook_format_changes(changes):
    """Format Git changes in the way Git hooks expect them in `stdin`.

    :param changes: a dict with keys are Git refs, and values are pairs
                    (old_sha, new_sha)
    :return: formatted changes ready to pipe to a Git hook
    """
    return '\n'.join(
        ' '.join((old_gitsha, new_gitsha, ref))
        for ref, (old_gitsha, new_gitsha) in changes.items())


SKIP = object()


class Hook(object):
    """Allow to call a GitLab hook.

    In Heptapod, we disable by default some of the Git hooks, in order to get
    finer control of them by calling them directly.

    This allows the Mercurial process to send accurate user information in
    its inner pushes to Git repos, as well as to notify GitLab of changes
    at the right stage of Mercurial transaction end.
    """

    def __init__(self, name, repo):
        self.name = name
        self.repo = repo
        self.git_fs_path = self.repo.root[:-3] + '.git'
        shell = repo.ui.config(b'heptapod', b'gitlab-shell')
        if not shell:
            raise RuntimeError("Path to GitLab Shell is unknown")
        self.gitlab_shell = shell

    def __str__(self):
        return "GitLab %r hook wrapper" % self.name

    def environ(self):
        base = self.repo.ui.environ
        if base.get('HEPTAPOD_SKIP_ALL_GITLAB_HOOKS', '').strip() == 'yes':
            return SKIP
        if base.get('HEPTAPOD_SKIP_GITLAB_HOOK', '').strip() == self.name:
            return SKIP

        gl_id = base.get('HEPTAPOD_USERINFO_ID')
        project_id = base.get('HEPTAPOD_PROJECT_ID')

        if gl_id is None:
            raise ValueError("User id not available")
        if project_id is None:
            raise ValueError("Project id not available")

        env = dict(os.environ)
        env['HG_GIT_SYNC'] = 'yes'
        env['GL_ID'] = 'user-' + gl_id
        # Protocol is only to deny access based on blocked protocol,
        # but 'web' is always accepted
        # (see gitlab_access.rb and protocol_access.rb
        # from gitlab-rails/lib/gitlab lib/gitlab)
        env['GL_PROTOCOL'] = 'web'
        env['GL_REPOSITORY'] = 'project-' + project_id
        return env

    def __call__(self, changes):
        """Call GitLab Hook for the given changes.

        :return: numeric return code, output and error.
                 The return code is like for a process does: 0 for success,
                 anything else for failures.
        """
        if not changes:
            self.repo.ui.debug(
                "%s: empty set of changes - nothing to do." % self)
            return 0, '', ''

        try:
            env = self.environ()
        except ValueError as exc:
            msg = "%s, not sending notifications!" % exc.args[0]
            self.repo.ui.warn("%s: %s" % (self, msg))
            return 1, '', msg

        if env is SKIP:
            self.repo.ui.note('%s: bailing (explicitely told not to send)')
            return 0, '', ''

        self.repo.ui.note("%s: sending changes %r" % (self, changes))
        pr = subprocess.Popen(
            [os.path.join(self.gitlab_shell, 'hooks', self.name)],
            env=env,
            cwd=self.git_fs_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)
        out, err = pr.communicate(input=git_hook_format_changes(changes))
        return pr.returncode, out, err
