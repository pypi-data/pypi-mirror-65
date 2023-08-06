#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy
import sys
import subprocess
import shutil
import platform


import distutils.spawn
from setuptools import setup, Extension
from setuptools.command.sdist import sdist


# make sure we are in the right directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

if not os.path.exists('duckdb.cpp'):
    prev_wd = os.getcwd()
    os.chdir('../..')
    subprocess.Popen('python scripts/amalgamation.py'.split(' ')).wait()
    os.chdir(prev_wd)
    shutil.copyfile('../../src/amalgamation/duckdb.hpp', 'duckdb.hpp')
    shutil.copyfile('../../src/amalgamation/duckdb.cpp', 'duckdb.cpp')


toolchain_args = ['-std=c++11']
#toolchain_args = ['-std=c++11', '-Wall', '-O0', '-g']

if platform.system() == 'Darwin':
    toolchain_args.extend(['-stdlib=libc++', '-mmacosx-version-min=10.7'])

class get_pybind_include(object):
    """Helper class to determine the pybind11 include path
    The purpose of this class is to postpone importing pybind11
    until it is actually installed, so that the ``get_include()``
    method can be invoked. """

    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11
        return pybind11.get_include(self.user)


libduckdb = Extension('duckdb',
    include_dirs=[numpy.get_include(), '.', get_pybind_include(), get_pybind_include(user=True)],
    sources=['duckdb_python.cpp', 'duckdb.cpp'],
    extra_compile_args=toolchain_args,
    extra_link_args=toolchain_args,
    language='c++')

# Only include pytest-runner in setup_requires if we're invoking tests
if {'pytest', 'test', 'ptr'}.intersection(sys.argv):
    setup_requires = ['pytest-runner']
else:
    setup_requires = []

setup(
    name = "duckdb",
    description = 'DuckDB embedded database',
    keywords = 'DuckDB Database SQL OLAP',
    url="https://www.duckdb.org",
    long_description = '',
    install_requires=[ # these versions are still available for Python 2, newer ones aren't
         'numpy>=1.14', 
         'pandas>=0.23',
         'pybind11>=2.4'
    ],
    packages=['duckdb_query_graph'],
    include_package_data=True,
    setup_requires=setup_requires + ["setuptools_scm"] + ['pybind11>=2.4'],
    use_scm_version = {"root": "../..", "relative_to": __file__},
    tests_require=['pytest'],
    classifiers = [
        'Topic :: Database :: Database Engines/Servers',
        'Intended Audience :: Developers'
    ],
    ext_modules = [libduckdb],
    maintainer = "Hannes Muehleisen",
    maintainer_email = "hannes@cwi.nl"
)
