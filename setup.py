#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages


setup(name='py_lru_cache',
      version='0.1.4',
      description="""LRU cache for python. Provides a dictionary-like object as well as a method decorator.""",
      author='Chris Stucchio',
      author_email='stucchio@gmail.com',
      license='Dual: GPL v3 or BSD',
      url='https://github.com/stucchio/Python-LRU-cache',
      packages = ['lru'],
     )
