# -*- coding: utf-8 -*-
"""PLOP Controller"""

from tg import expose

from erebot.lib.base import BaseController

__all__ = ['PlopController']

class PlopController(BaseController):
    """
    The controller for PLOP (Python Logging On PHP).
    """
    @expose('erebot.templates.plop.index')
    def index(self):
        """Handle the front-page."""
        return dict()

