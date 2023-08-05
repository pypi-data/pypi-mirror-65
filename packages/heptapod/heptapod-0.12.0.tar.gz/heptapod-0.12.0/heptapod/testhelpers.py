# Copyright 2019 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Helpers for automatic tests.

These allow both high level operation on testing repos, and lower level
calls and introspections, making it possible to test more exhaustively inner
code paths that with `.t` tests, which are really functional tests.
"""
import os
from mercurial import (
    cmdutil,
    commands,
    hg,
    node,
    phases,
    ui as uimod,
)
import random

# re-exports for stability
NULL_REVISION = node.nullrev
NULL_ID = node.nullid


def make_ui(base_ui, config=None):
    # let's make sure we aren't polluted by surrounding settings
    os.environ['HGRCPATH'] = ''
    if base_ui is None:
        ui = uimod.ui.load()
    else:
        ui = base_ui.copy()
    if ui.environ is os.environ:
        ui.environ = dict(ui.environ)
    if config is not None:
        for section_name, section in config.items():
            for item_name, item_value in section.items():
                ui.setconfig(section_name, item_name, item_value,
                             source='tests')
    return ui


class LocalRepoWrapper(object):

    def __init__(self, repo):
        self.repo = repo

    @classmethod
    def init(cls, path, base_ui=None, config=None):
        path = str(path)
        init = cmdutil.findcmd('init', commands.table)[1][0]
        ui = make_ui(base_ui, config)
        init(ui, dest=path)
        return cls(hg.repository(ui, path))

    @classmethod
    def load(cls, path, base_ui=None, config=None):
        path = str(path)
        ui = make_ui(base_ui, config=config)
        return cls(hg.repository(ui, path))

    @classmethod
    def share_from_path(cls, src_path, dest_path,
                        ui=None, base_ui=None, config=None,
                        **share_opts):
        """Create a new repo as the `share` command would do.

        :param ui: if specified, will be copied and used for the new repo
                   creation through ``share``
        :param config: only if ``ui`` is not specified, will be used to
                       create a new ``ui`` instance
        :param base_ui: only if ``ui`` is not specified, will be used to
                       create a new :class:`ui` instance
        :param share_opts: passed directly to :func:`hg.share()`
        :return: wrapper for the new repo
        """
        if ui is None:
            ui = make_ui(base_ui, config=config)
        else:
            ui = ui.copy()

        # the 'share' command defined by the 'share' extension, is just a thin
        # wrapper around `hg.share()`, which furthermore returns a repo object.
        return cls(hg.share(ui, str(src_path), dest=str(dest_path),
                            **share_opts))

    def share(self, dest_path, **share_opts):
        return self.share_from_path(self.repo.root, dest_path,
                                    ui=self.repo.ui, **share_opts)

    def command(self, name, *args, **kwargs):
        cmd = cmdutil.findcmd(name, commands.table)[1][0]
        repo = self.repo
        return cmd(repo.ui, repo, *args, **kwargs)

    def write_commit(self, rpath,
                     content=None, message=None,
                     return_ctx=False,
                     parent=None,
                     branch=None,
                     topic=None):
        """Write content at rpath and commit in one call.

        This is meant to allow fast and efficient preparation of
        testing repositories. To do so, it goes a bit lower level
        than the actual commit command, so is not suitable to test specific
        commit options, especially if through extensions.

        This leaves the working directoy updated at the new commit.

        :param rpath: relative path from repository root. If existing,
                      will be overwritten by `content`
        :param content: what's to be written in ``rpath``.
                        If not specified, will be replaced by random content.
        :param message: message commit. If not specified, defaults to
                        ``content``
        :param parent: binary node value. If specified, the repository is
                       updated to it first. Useful to produce branching
                       histories. This is single valued, because the purpose
                       of this method is not to produce merge commits.
        :returns: binary node for the resulting commit.
        """
        rpath = str(rpath)
        repo = self.repo
        path = os.path.join(repo.root, rpath)
        if parent is not None:
            self.update_bin(parent)
        if content is None:
            content = "random: {}\n\nparent: {}\n".format(
                random.random(),
                node.hex(repo.dirstate.p1()))
        if message is None:
            message = content

        if branch is not None:
            self.repo.dirstate.setbranch(branch)

        if topic is not None:
            self.command('topics', topic)

        flags = 'wb' if isinstance(content, bytes) else 'w'
        with open(path, flags) as fobj:
            fobj.write(content)

        def commitfun(ui, repo, message, match, opts):
            return self.repo.commit(message,
                                    opts.get('user'),
                                    opts.get('date'),
                                    match=match,
                                    editor=False,
                                    extra=None)
        new_node = cmdutil.commit(repo.ui, repo, commitfun, (path, ),
                                  dict(addremove=True,
                                       message=message))
        return repo[new_node] if return_ctx else new_node

    def update_bin(self, bin_node, **opts):
        """Update to a revision specified by its node in binary form.

        This is separated in order to avoid ambiguities
        """
        # maybe we'll do something lower level later
        self.update(node.hex(bin_node), **opts)

    def update(self, rev, hidden=False):
        repo = self.repo.unfiltered() if hidden else self.repo
        cmdutil.findcmd('update', commands.table)[1][0](repo.ui, repo, rev)

    def set_phase(self, phase_name, revs, force=True):
        repo = self.repo
        opts = dict(force=force, rev=revs)
        opts.update((phn, phn == phase_name) for phn in phases.cmdphasenames)
        cmdutil.findcmd('phase', commands.table)[1][0](repo.ui, repo, **opts)

    def prune(self, revs, successors=(), bookmarks=()):
        # the prune command expects to get all these arguments (it relies
        # on the CLI defaults but doesn't have any at the function call level).
        # They are unconditionally concatened to lists, hence must be lists.
        # (as of Mercurial 5.3.1)
        if isinstance(revs, (bytes, str)):
            revs = [revs]
        return self.command('prune', rev=revs,
                            new=[],  # deprecated yet expected
                            successor=list(successors),
                            bookmark=list(bookmarks))
