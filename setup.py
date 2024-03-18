#!/usr/bin/env python
# -*- coding: utf-8 -*-

import warnings
import os
import io
import re

try:
  from setuptools import setup
  from setuptools.command.install import install
  setup
except ImportError:
  from distutils.core import setup
  setup

# Get the long description from the README
def readme():
  with open('README.md') as f:
    return f.read()

# Read, version funcs taken from:
# https://github.com/ellisonbg/altair/blob/master/setup.py
def read(path, encoding='utf-8'):
    path = os.path.join(os.path.dirname(__file__), path)
    with io.open(path, encoding=encoding) as fp:
        return fp.read()

def version(path):
    """
    Obtain the packge version from a python file e.g. pkg/__init__.py
    See <https://packaging.python.org/en/latest/single_source_version.html>.
    """
    version_file = read(path)
    version_match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


VERSION = version('majerus/__init__.py')

# Setup!
setup(name = 'majerus',
      version = VERSION,
      description = 'Machine learning predictions for college basketball games',
      long_description = readme(),
      classifiers = [
                      'Development Status :: 1 - Alpha',
                      'Programming Language :: Python :: 3.9',
                      'Programming Language :: Python :: 3.10'
                    ],
      author = 'David P. Fleming, PhD',
      author_email = 'dpfleming91@gmail.com',
      license = 'Personal',
      packages = ['majerus'],
      install_requires = ['numpy',
                          'matplotlib',
                          'pandas',
                          'pytest',
                          'scipy',
                          'scikit-learn',
                          'mechanicalsoup',
                          'beautifulsoup4',
                          'lxml',
                          'html5lib'],
      include_package_data = False,
      zip_safe = False)
