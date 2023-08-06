# -*- coding: utf-8 -*-
"""
:Authors: cykooz
:Date: 14.04.2020
"""
from __future__ import print_function, unicode_literals

import os
from collections import namedtuple

import pytest
import zc.buildout.testing
import setuptools.wheel
from . import extension


ORIGIN_NAMESPACE_PACKAGE_INIT = setuptools.wheel.NAMESPACE_PACKAGE_INIT

BUILDOUT_CFG = '''
[buildout]
extensions = cykooz.buildout.fixnamespace
eggs-directory = eggs
download-cache = download
#install-from-cache = true
newest = false
abi-tag-eggs = false
versions = versions
parts = packages

[packages]
recipe = zc.recipe.egg:eggs
eggs = zope.interface

[versions]
setuptools = 44.0.0
'''


@pytest.fixture(name='buildout_env')
def buildout_env_fixture():
    TestEnv = namedtuple('TestEnv', ['globs'])
    test_env = TestEnv(globs={})
    zc.buildout.testing.buildoutSetUp(test_env)
    buildout_dir = test_env.globs['sample_buildout']
    download_cache = os.path.join(buildout_dir, 'download', 'dist')
    os.makedirs(download_cache)
    src_path = os.path.abspath(__file__)
    for _ in range(4):
        src_path = os.path.dirname(src_path)
    zc.buildout.testing.sdist(src_path, download_cache)
    try:
        yield test_env.globs
    finally:
        zc.buildout.testing.buildoutTearDown(test_env)


def test_extension(buildout_env):
    assert setuptools.wheel.NAMESPACE_PACKAGE_INIT == ORIGIN_NAMESPACE_PACKAGE_INIT

    sample_buildout = buildout_env['sample_buildout']
    write = buildout_env['write']
    system = buildout_env['system']
    buildout = buildout_env['buildout']

    write(sample_buildout, 'buildout.cfg', BUILDOUT_CFG)
    res = system(buildout)
    assert 'Monkey-patching setuptools to fix content of namespace-file' in res

    eggs_dir = os.path.join(sample_buildout, 'eggs')
    for name in os.listdir(eggs_dir):
        if name.startswith('zope.interface-'):
            path = os.path.join(eggs_dir, name, 'zope', '__init__.py')
            content = open(path, 'rt').read()
            assert content == extension.NAMESPACE_PACKAGE_INIT
            break
