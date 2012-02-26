# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect
from pylons.i18n import ugettext as _, lazy_ugettext as l_, N_
from repoze.what import predicates
from pkg_resources import resource_filename

from erebot import model

from erebot.lib.base import BaseController
#from tgrum import RumAlchemyController
from erebot.controllers.error import ErrorController
from erebot.controllers.plop import PlopController
from erebot.controllers.xmlns import XmlnsController
from erebot.controllers.buildbot import BuildbotController

__all__ = ['RootController']

class RootController(BaseController):
    """
    The root controller for the Erebot application.
    """
    error = ErrorController()
#    admin = RumAlchemyController(model, predicates.has_permission(
#        'manage', msg=l_('Only for people with the "manage" permission')),
#        resource_filename('erebot.templates', ''), config={
#            'rum.translator': {
#                'use': 'erebot',
#            },
#            'templating': {
#                'renderer': 'erebot',
#            },
#        }
#    )
    buildbot = BuildbotController()
    plop = PlopController()
    xmlns = XmlnsController()

    @expose('erebot.templates.root.index')
    def index(self):
        """Handle the front-page."""
        return dict()

    @expose('erebot.templates.root.development')
    def development(self):
        """Prints information and links for development-related resources."""
        import urllib2
        import json

        req = urllib2.Request(
            'http://localhost:8010/json/builders/Core/builds/-1/?compact=1',
            headers={'Content-Type': 'application/json'},
        )
        build = {}
        urls = {}
        try:
            build = json.load(urllib2.urlopen(req), 'latin-1')
        except urllib2.URLError:
            pass

        res = build.get('text', ['retry'])
        for step in build.get('steps', {}):
            if 'urls' in step:
                urls.update(step['urls'])

        mapping = {
            'build successful': N_('success'),
            'warnings':         N_('warnings'),
            'failed':           N_('failure'),
            'skipped':          N_('skipped'),
            'exception':        N_('exception'),
            'build exception':  N_('exception'),
            'retry':            N_('retry'),
            '':                 N_('retry'),
        }

        while ' '.join(res) not in mapping:
            res.pop()
        res = ' '.join(res)

        return dict(
            status_text=_(mapping[res]),
            status_code=res,
            status_class=mapping[res],
            urls=urls,
        )

    @expose('erebot.templates.login')
    def login(self, came_from=url('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(login_counter=str(login_counter),
                    came_from=came_from)

