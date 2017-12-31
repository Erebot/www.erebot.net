# -*- coding: utf-8 -*-
"""XMLNS Controller"""

from tg import expose

from erebot.lib.base import BaseController

__all__ = ['XmlnsController']

class XmlnsController(BaseController):
    """
    The controller for namespace information.
    """
    @expose('erebot.templates.xmlns.index')
    def index(self):
        """Handle the front-page."""
        return dict()

    @expose('erebot.templates.xmlns.erebot')
    def erebot(self):
        return dict()

    @expose('erebot.templates.xmlns.logging')
    def logging(self):
        return dict()

