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
        return dict()

    @expose('erebot.templates.login')
    def login(self, came_from=url('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(login_counter=str(login_counter),
                    came_from=came_from)

