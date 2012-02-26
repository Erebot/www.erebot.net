# -*- coding: utf-8 -*-
"""
"""
from __future__ import absolute_import

from genshi.filters import Translator
from genshi.template import TemplateLoader
from rum.i18n import RumTranslator
from rum.templating.genshi_renderer import GenshiRenderer, add_lang_attrs
from pylons.i18n import ugettext as pylons_ugettext, \
                        ungettext as pylons_ungettext

class ErebotRumTranslator(RumTranslator):
    _NAME = "ErebotRumTranslator"

    def ugettext(self, txt, project='all'):
        res = pylons_ugettext(txt)
        return res != txt and res or \
            super(ErebotRumTranslator, self).ugettext(txt, project)

    def ungettext(self, singular, plural, n, project='all'):
        res = pylons_ungettext(singular, plural, n)
        return (res != singular and res != plural) and res or \
            super(ErebotRumTranslator, self).ugettext(
                singular, plural, n, project)

class ErebotRumGenshiRenderer(GenshiRenderer):
    method = 'xhtml'
    framework_name = 'genshi-xml'

    def __init__(self, search_path=None, auto_reload=True, cache_dir=None,
                 method=method):
        super(GenshiRenderer, self).__init__(search_path, auto_reload,
                                             cache_dir)
        self.method = method or self.method

        def _add_filter(tpl):
            tpl.filters.insert(0, add_lang_attrs)
            tpl.filters.insert(0, Translator(pylons_ugettext))

        self.loader = TemplateLoader(
            search_path = self.search_path,
            auto_reload = self.auto_reload,
            callback = _add_filter,
        )

    def render(self, data, possible_templates=[]):
        template =  self.load_template(possible_templates)
        return template.generate(**data).render(method=self.method,
                                                encoding=None)

