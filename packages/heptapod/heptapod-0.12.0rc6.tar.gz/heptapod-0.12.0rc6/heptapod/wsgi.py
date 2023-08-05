# heptapod/hgweb.py - Heptapod HTTP interface for a directory of repositories.
#
# derived under GPL2+ from Mercurial's hgwebdir_mod.py, whose
# copyright holders are
#   Copyright 21 May 2005 - (c) 2005 Jake Edge <jake@edge2.net>
#   Copyright 2005, 2006 Matt Mackall <mpm@selenic.com>
#
# This file Copyright 2019 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from __future__ import absolute_import

import logging
import gc
import os

from mercurial.i18n import _

from mercurial.hgweb.common import (
    ErrorResponse,
    HTTP_SERVER_ERROR,
    HTTP_NOT_FOUND,
    cspvalues,
    statusmessage,
)

from mercurial import (
    encoding,
    error,
    extensions,
    hg,
    profiling,
    pycompat,
    ui as uimod,
)

from mercurial.hgweb import (
    hgweb_mod,
    request as requestmod,
)

logger = logging.getLogger(__name__)
# logging configuration will be initialized from the Mercurial global
# configuration, overriding this:
logging.basicConfig(level=logging.INFO)

ALLOWED_REMOTES = (
    '127.0.0.1',
    '::1',
    '',  # Unix Domain Socket
    )


# Suffixes of HTTP headers that are directly forwarded in environment
FORWARDED_HEADERS_SUFFIXES = (
    'USERINFO_ID',
    'USERINFO_USERNAME',
    'USERINFO_NAME',
    'USERINFO_EMAIL',
    'PROJECT_ID',
    'PROJECT_PATH',
    'PROJECT_NAMESPACE_FULL_PATH',
    )


class HgServe(object):
    """WSGI application serving repositories under a given root path

    The repositories are expected in the `heptapod.repositories-root`
    Mercurial configuration.

    This works under full trust of the incoming request: callers are either
    `gitlab-rails` or `gitlab-workhorse`.
    """
    def __init__(self, conf_path=None, baseui=None):
        self.baseui = baseui
        if baseui:
            self.ui = baseui.copy()
        else:
            self.ui = uimod.ui.load()
        self.motd = None
        if not baseui:
            # set up environment for new ui
            extensions.loadall(self.ui)
            extensions.populateui(self.ui)
        if conf_path is not None:
            for i, rcf in enumerate(conf_path.split(':')):
                if i == 0 and not os.path.exists(rcf):
                    raise error.Abort(_('config file %s not found!') % rcf)
                logger.info("Loading configuration from %r", rcf)
                self.ui.readconfig(rcf, trust=True)

        root = self.ui.config('heptapod', 'repositories-root')
        if root is None:
            raise ValueError("heptapod.repositories-root is not configured.")
        self.repos_root = root

    def apply_heptapod_headers(self, environ):
        perm_user = environ.get('HTTP_X_HEPTAPOD_PERMISSION_USER')
        if perm_user is not None and environ['REMOTE_ADDR'] in ALLOWED_REMOTES:
            environ['REMOTE_USER'] = perm_user
        for hepta_key in FORWARDED_HEADERS_SUFFIXES:
            hepta_val = environ.pop('HTTP_X_HEPTAPOD_' + hepta_key, None)
            if hepta_val is not None:
                environ['HEPTAPOD_' + hepta_key] = hepta_val

    def __call__(self, env, respond):
        baseurl = self.ui.config('web', 'baseurl')
        self.apply_heptapod_headers(env)
        req = requestmod.parserequestfromenv(env, altbaseurl=baseurl)
        res = requestmod.wsgiresponse(req, respond)
        return self.run_wsgi(req, res)

    def run_wsgi(self, req, res):
        profile = self.ui.configbool('profiling', 'enabled')
        with profiling.profile(self.ui, enabled=profile):
            try:
                for r in self._runwsgi(req, res):
                    yield r
            finally:
                # There are known cycles in localrepository that prevent
                # those objects (and tons of held references) from being
                # collected through normal refcounting. We mitigate those
                # leaks by performing an explicit GC on every request.
                # TODO remove this once leaks are fixed.
                # TODO only run this on requests that create localrepository
                # instances instead of every request.
                gc.collect()

    def load_repo(self, uri_path):
        repo_path = os.path.join(self.repos_root, uri_path)
        if not os.path.isdir(os.path.join(repo_path, '.hg')):
            # hg.repository() would raise a RepoError which is
            # not qualified enough to distinguish it cleanly (just
            # the message)
            raise ErrorResponse(HTTP_NOT_FOUND, "Not Found")
        logger.info("loading repo at %r", repo_path)
        # ensure caller gets private copy of ui
        return hg.repository(self.ui.copy(), repo_path)

    def _runwsgi(self, req, res):
        try:
            csp = cspvalues(self.ui)[0]
            if csp:
                res.headers['Content-Security-Policy'] = csp

            uri_path = req.dispatchpath.strip('/')
            # Re-parse the WSGI environment to take into account our
            # repository path component.
            uenv = req.rawenv
            req = requestmod.parserequestfromenv(
                uenv, reponame=uri_path,
                altbaseurl=self.ui.config('web', 'baseurl'),
                # Reuse wrapped body file object otherwise state
                # tracking can get confused.
                bodyfh=req.bodyfh)
            try:
                repo = self.load_repo(uri_path)
                return hgweb_mod.hgweb(repo).run_wsgi(req, res)
            except IOError as inst:
                msg = encoding.strtolocal(inst.strerror)
                raise ErrorResponse(HTTP_SERVER_ERROR, msg)
            except error.RepoError as inst:  # pragma: no cover
                # This case can't happen because hgweb_mod catches them
                # already. To be removed in Heptapod 0.8
                raise ErrorResponse(HTTP_SERVER_ERROR, bytes(inst))

        except ErrorResponse as e:
            # To be carefully tested with Python3, but Heptapod is running py2
            # for the time being (suitable py3 version not available yet)

            # This is a dubious part from hgweb: the status message includes
            # the error message, but that can get funky because of potential
            # translation. Common practice would be just to repeat the
            # generic meaning of the code, e.g, "NOT FOUND"
            # and provide details in the reponse body
            res.status = statusmessage(e.code, pycompat.bytestr(e))
            res.headers['Content-Type'] = 'text/plain; encoding={}'.format(
                pycompat.sysstr(encoding.encoding))
            res.setbodygen((e.message or b'') + b"\n")
            return res.sendresponse()

    @classmethod
    def default_app(cls):
        HEPTAPOD_HGRC = os.environ.get('HEPTAPOD_HGRC')
        if HEPTAPOD_HGRC:
            return HgServe(conf_path=HEPTAPOD_HGRC)


hgserve = HgServe.default_app()
