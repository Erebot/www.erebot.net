# -*- coding: utf-8 -*-
"""WSGI environment setup for Erebot."""

import tg
from erebot.config.app_cfg import base_config

__all__ = ['load_environment']

#Use base_config to setup the environment loader function
load_environment = base_config.make_load_environment()

class expose(tg.expose):
    def __pre_render(self, *args, **kwargs):
        from tg import tmpl_context
        tmpl_context.page = self.page

    def __call__(self, func):
        from tg.decorators import Decoration
        self.page = '%s:%s' % (func.__module__, func.__name__)
        deco = Decoration.get_decoration(func)
        deco.register_hook('before_render', self.__pre_render)
        return super(expose, self).__call__(func)
tg.expose = expose

