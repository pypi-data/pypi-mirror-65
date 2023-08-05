# Copyright 2019-2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from mercurial import (
    configitems,
    error,
    scmutil,
    phases,
)

if 'allow-publish' not in configitems.coreitems['web']:
    configitems._register(configitems.coreitems,
                          section='web',
                          name='allow-publish',
                          alias=[('web', 'allow_publish')],
                          default=lambda: list(['*']),
                          )


def validate_hook_type(expected, hooktype=None, **kw):
    """Check that the hook has the expected type, and raise if not.

    It is really important that permission check hooks get executed
    in the right position (pretxnopen, pretxclose).

    For example, it's better to reject invalid writes right away than to
    rollback them, for efficiency and security (smaller attack surface).

    It's also a matter of having the right information at disposal.

    Example usage::

      >>> from heptapod.hooks import perm
      >>> def the_hook(repo, *args, **kwargs):
      ...     perm.validate_hook_type('precommit', **kwargs)
      ...     return 0  # success

    ``repo`` is not needed for our example, and actually that proves it won't
    be used at all::

      >>> repo = None

      >>> the_hook(None, hooktype='precommit')
      0
      >>> the_hook(None, hooktype='postxn') # doctest: +IGNORE_EXCEPTION_DETAIL
      Traceback (most recent call last):
      ProgrammingError: This hook must be used as 'precommit', not 'postxn'.

    :param expected: the proper hook type, e.g, ``pretxnopen``.
    :param hooktype: should be passed straight from hook kwargs
    """
    if hooktype == expected:
        return
    raise error.ProgrammingError(
        "This hook must be used as a %r, not %r" % (expected, hooktype))


def get_remote_user(repo):
    """Return remote user name, or `None`

    within Heptapod, the absence of a remote user means that `hg` is invoked
    from the command line, or directly by a server-side process, such as
    the Rails application performing a merge.

    Hence `None` implies to skip all permission checks.
    """
    return repo.ui.environ.get("REMOTE_USER", None)


def allowed(repo, remote_user, config_group, config_item):
    """Read from repo config list to check if given user is allowed.

    within Heptapod, ``remote_user`` being ``None`` means that `hg` is invoked
    from the command line, or directly by a server-side process, such as
    the Rails application performing a merge.

    In these cases, the permission
    checking responsibility is on the caller. Hence a ``None`` remote user
    is always allowed.
    """
    allowed = repo.ui.configlist(config_group, config_item)

    if remote_user is None or '*' in allowed or remote_user in allowed:
        repo.ui.debug('user %r is allowed by %s.%s=%r' % (
            remote_user, config_group, config_item, allowed))
        return True

    return False


def check_write(repo, *args, **kwargs):
    """Check that remote user has write privileges.

    In this hook, the very fact to be called serves as detection that a
    write operation will happen.

    Therefore the implementation is very straightforward.
    """
    validate_hook_type('pretxnopen', **kwargs)

    remote_user = get_remote_user(repo)
    if remote_user is not None:
        repo.ui.debug(
            'check_write detected push from user: %r\n' % remote_user)

    if allowed(repo, remote_user, 'web', 'allow-push'):
        return 0

    msg = 'user %r does not have write permission' % remote_user
    repo.ui.note(msg)
    repo.ui.status(msg)
    return 1


def check_publish(repo, *args, **kwargs):
    validate_hook_type('pretxnclose', **kwargs)
    remoteuser = get_remote_user(repo)

    if remoteuser is not None:
        repo.ui.debug(
            'check_publish detected push from user: %r\n' % remoteuser)

    if allowed(repo, remoteuser, 'web', 'allow-publish'):
        # we have nothing more to check
        return 0

    tr = repo.currenttransaction()
    assert tr is not None and tr.running()
    phaseschanges = tr.changes.get("phases", {})
    publishing = set(rev for rev, (old, new) in phaseschanges.iteritems()
                     if new == phases.public and old != phases.public)
    if publishing:
        node = repo.changelog.node
        nodes = [node(r) for r in sorted(publishing)]
        nodes = scmutil.nodesummaries(repo, nodes)
        msg = 'user "%s" is not authorised to publish changesets: %s\n'
        raise error.Abort(msg % (remoteuser, nodes))
    return 0
