# -*- coding: utf-8 -*-
"""Unit and functional test suite for Erebot."""

from os import path
import sys

from tg import config
from paste.deploy import loadapp
from paste.script.appinstall import SetupCommand
from routes import url_for
from webtest import TestApp
from nose.tools import eq_

__all__ = ['TestController', 'url_for']

class TestController(object):
    """
    Base functional test case for the controllers.
    """
    application_under_test = 'main_without_authn'

    def setUp(self):
        """Method called by nose before running each test"""
        # Loading the application:
        conf_dir = config.here
        wsgiapp = loadapp('config:test.ini#%s' % self.application_under_test,
                          relative_to=conf_dir)
        self.app = TestApp(wsgiapp)
        # Setting it up:
        test_file = path.join(conf_dir, 'test.ini')
        cmd = SetupCommand('setup-app')
        cmd.run([test_file])
