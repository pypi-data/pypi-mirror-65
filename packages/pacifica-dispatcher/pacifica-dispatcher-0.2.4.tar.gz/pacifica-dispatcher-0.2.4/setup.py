#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Setup and install the pacifica service."""
from os import path
try:  # pip version 9
    from pip.req import parse_requirements
except ImportError:
    from pip._internal.req import parse_requirements
from setuptools import setup, find_packages

# parse_requirements() returns generator of pip.req.InstallRequirement objects
INSTALL_REQS = parse_requirements('requirements.txt', session='hack')

setup(
    name='pacifica-dispatcher',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description='Pacifica Dispatcher',
    url='https://github.com/pacifica/pacifica-dispatcher/',
    long_description=open(path.join(
        path.abspath(path.dirname(__file__)),
        'README.md')).read(),
    long_description_content_type='text/markdown',
    author='Mark Borkum',
    author_email='mark.borkum@pnnl.gov',
    packages=find_packages(include=['pacifica.*']),
    namespace_packages=['pacifica'],
    install_requires=[str(ir.req) for ir in INSTALL_REQS]
)
