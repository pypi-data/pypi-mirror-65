# -*- coding: utf-8 -*-
"""
:Authors: cykooz
:Date: 14.04.2020
"""
import logging


NAMESPACE_PACKAGE_INIT = "__path__ = __import__('pkgutil').extend_path(__path__, __name__)\n"


def extension(buildout=None):
    logger = logging.getLogger('zc.buildout')
    logger.info(
        'Monkey-patching setuptools to fix content of namespace-file of '
        'packages which will be installed from wheel.'
    )
    import setuptools.wheel
    setuptools.wheel.NAMESPACE_PACKAGE_INIT = NAMESPACE_PACKAGE_INIT
