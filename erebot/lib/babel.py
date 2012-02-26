#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import tempfile
import shutil

from distutils import log
from distutils.cmd import Command
from distutils.errors import DistutilsOptionError, DistutilsSetupError

from babel.messages.pofile import read_po, write_po

class update_catalog(Command):
    """Catalog merging command for use in ``setup.py`` scripts.

    If correctly installed, this command is available to Setuptools-using
    setup scripts automatically. For projects using plain old ``distutils``,
    the command needs to be registered explicitly in ``setup.py``::

        from babel.messages.frontend import update_catalog

        setup(
            ...
            cmdclass = {'update_catalog': update_catalog}
        )

    :since: version 0.9
    :see: `Integrating new distutils commands <http://docs.python.org/dist/node32.html>`_
    :see: `setuptools <http://peak.telecommunity.com/DevCenter/setuptools>`_
    """

    description = 'update message catalogs from a POT file'
    user_options = [
        ('domain=', 'D',
         "domain of PO file (default 'messages')"),
        ('input-file=', 'i',
         'name of the input file'),
        ('output-dir=', 'd',
         'path to base directory containing the catalogs'),
        ('output-file=', 'o',
         "name of the output file (default "
         "'<output_dir>/<locale>/LC_MESSAGES/<domain>.po')"),
        ('locale=', 'l',
         'locale of the catalog to compile'),
        ('ignore-obsolete=', None,
         'whether to omit obsolete messages from the output'),
        ('no-fuzzy-matching', 'N',
         'do not use fuzzy matching'),
        ('previous', None,
         'keep previous msgids of translated messages'),
        ('identity=', None,
         'locale of the identity catalog'),
    ]
    boolean_options = ['ignore_obsolete', 'no_fuzzy_matching', 'previous']

    def initialize_options(self):
        self.domain = 'messages'
        self.input_file = None
        self.output_dir = None
        self.output_file = None
        self.locale = None
        self.ignore_obsolete = False
        self.no_fuzzy_matching = False
        self.previous = False
        self.identity = None

    def finalize_options(self):
        if not self.input_file:
            raise DistutilsOptionError('you must specify the input file')
        if not self.output_file and not self.output_dir:
            raise DistutilsOptionError('you must specify the output file or '
                                       'directory')
        if self.output_file and not self.locale:
            raise DistutilsOptionError('you must specify the locale')
        if self.no_fuzzy_matching and self.previous:
            self.previous = False

    def run(self):
        po_files = []
        if not self.output_file:
            if self.locale:
                po_files.append((self.locale,
                                 os.path.join(self.output_dir, self.locale,
                                              'LC_MESSAGES',
                                              self.domain + '.po')))
            else:
                for locale in os.listdir(self.output_dir):
                    po_file = os.path.join(self.output_dir, locale,
                                           'LC_MESSAGES',
                                           self.domain + '.po')
                    if os.path.exists(po_file):
                        po_files.append((locale, po_file))
        else:
            po_files.append((self.locale, self.output_file))

        domain = self.domain
        if not domain:
            domain = os.path.splitext(os.path.basename(self.input_file))[0]

        infile = open(self.input_file, 'U')
        try:
            template = read_po(infile)
        finally:
            infile.close()

        if not po_files:
            raise DistutilsOptionError('no message catalogs found')

        for locale, filename in po_files:
            log.info('updating catalog %r based on %r', filename,
                     self.input_file)
            infile = open(filename, 'U')
            try:
                catalog = read_po(infile, locale=locale, domain=domain)
            finally:
                infile.close()

            if locale == self.identity:
                # Do not use fuzzy matching for identity catalog
                # since we will provide sensible messages as necessary.
                catalog.update(template, True)

                log.info('translating identity catalog %r based on %r',
                    filename, self.input_file)
                for msg in catalog:
                    if not msg.string:
                        msg.string = msg.id
            else:
                catalog.update(template, self.no_fuzzy_matching)

            tmpname = os.path.join(os.path.dirname(filename),
                                   tempfile.gettempprefix() +
                                   os.path.basename(filename))
            tmpfile = open(tmpname, 'w')
            try:
                try:
                    write_po(tmpfile, catalog,
                             ignore_obsolete=self.ignore_obsolete,
                             include_previous=self.previous)
                finally:
                    tmpfile.close()
            except:
                os.remove(tmpname)
                raise

            try:
                os.rename(tmpname, filename)
            except OSError:
                # We're probably on Windows, which doesn't support atomic
                # renames, at least not through Python
                # If the error is in fact due to a permissions problem, that
                # same error is going to be raised from one of the following
                # operations
                os.remove(filename)
                shutil.copy(tmpname, filename)
                os.remove(tmpname)

