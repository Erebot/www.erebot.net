# -*- coding: utf-8 -*-
#quckstarted Options:
#
# sqlalchemy: True
# auth:       sqlalchemy
# mako:       False
#
#

import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

testpkgs=['WebTest >= 1.2.3',
               'nose',
               'coverage',
               'wsgiref',
               'repoze.who-testutil >= 1.0.1',
               ]
if sys.version_info[:2] == (2,4):
    testpkgs.extend(['hashlib', 'pysqlite'])

setup(
    name='Erebot',
    version='0.1',
    description='',
    author='',
    author_email='',
    #url='',
    install_requires=[
        "TurboGears2 >= 2.1.1",
        "Genshi",
        "zope.sqlalchemy >= 0.4",
        "repoze.tm2 >= 1.0a5",
        "sqlalchemy",
        "sqlalchemy-migrate",
        "repoze.what-quickstart",
        "repoze.what >= 1.0.8",
        "repoze.who-friendlyform >= 1.0.4",
        "repoze.what-pylons >= 1.0",
        "repoze.what.plugins.sql",
        "repoze.who==1.0.19",
        "tgext.admin >= 0.3.9",
        "tw.forms",
#        "rum",
#        "TgRum",
        "Babel >=0.9.4",
        "tg.devtools", # Required during bootstrap.
        "MySQL-python <= 1.2.3",
    ],
    setup_requires=["PasteScript >= 1.7"],
    paster_plugins=['PasteScript', 'Pylons', 'TurboGears2', 'tg.devtools'],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=testpkgs,
    package_data={'erebot': ['i18n/*/LC_MESSAGES/*.mo',
                                 'templates/*/*',
                                 'public/*/*']},
    message_extractors={'erebot': [
            ('**.py', 'python', None),
            ('templates/**.html', 'genshi', None),
            ('public/**', 'ignore', None)]},

    entry_points="""
    [paste.app_factory]
    main = erebot.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller

    [distutils.commands]
    update_catalog = erebot.lib.babel:update_catalog

    [rum.translator]
    erebot = erebot.lib.rum:ErebotRumTranslator

    [rum.renderers]
    erebot = erebot.lib.rum:ErebotRumGenshiRenderer
    """,
    dependency_links=[
        "http://www.turbogears.org/2.1/downloads/current/"
        ],
    zip_safe=False
)

