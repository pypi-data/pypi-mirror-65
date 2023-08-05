# Copyright 2019-2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later


def switch_user(wrapper, user):
    """Common method to change the name of the acting user.

    This helps enforcing that it works uniformly for all permission
    related hooks.
    """
    wrapper.repo.ui.environ['REMOTE_USER'] = user
