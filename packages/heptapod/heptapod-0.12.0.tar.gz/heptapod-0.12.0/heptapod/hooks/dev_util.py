# Copyright 2019-2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later


def print_heptapod_env(repo, *args, **kwargs):
    repo.ui.status(repr(sorted(
        (k, v) for (k, v) in repo.ui.environ.items()
        if k.startswith('HEPTAPOD_'))))
    return 0
