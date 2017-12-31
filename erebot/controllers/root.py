# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose

from erebot.lib.base import BaseController
from erebot.controllers.error import ErrorController
from erebot.controllers.plop import PlopController
from erebot.controllers.xmlns import XmlnsController

__all__ = ['RootController']

class RootController(BaseController):
    """
    The root controller for the Erebot application.
    """
    error = ErrorController()
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

