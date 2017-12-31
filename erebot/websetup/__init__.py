# -*- coding: utf-8 -*-
"""Setup the Erebot application"""

import logging

from erebot.config.environment import load_environment

__all__ = ['setup_app']

log = logging.getLogger(__name__)

import bootstrap

def setup_app(command, conf, vars):
    """Place any commands to setup erebot here"""
    load_environment(conf.global_conf, conf.local_conf)
    bootstrap.bootstrap(command, conf, vars)
