#!/usr/bin/env python3
from setuptools import setup, find_packages
import sys
import os
import re

def parse_requirements():
    requires = []
    with open('requirements.txt', 'r') as fr :
        for line in fr :
            pkg = line.strip()
            if pkg.startswith('git+'):
                pip_install_git(pkg)
            else:
                requires.append(pkg)
    return requires

def pip_install_git(link):
    os.system('pip install --upgrade {}'.format(link))
    return


with open('src/aiWT/__init__.py') as fd :
    lines = fd.read()
    __version__ = re.search('__version__ = "(.*)"', lines).group(1)
    __author__ = re.search('__author__ = "(.*)"', lines).group(1)
    __contact__ = re.search('__contact__ = "(.*)"', lines).group(1)
    __license__ = re.search('__license__ = "(.*)"', lines).group(1)

assert sys.version_info >= (3, 6)
description = "Python3 packages for Kinetic Energy Density FUnctional with DFTpy"

with open('README.md') as fh :
    long_description = fh.read()


release = 0
VERSION = {'version' : __version__}
# if release :
#     VERSION = {'version' : __version__}
# else :
#     VERSION = {
#             'use_scm_version': {'version_scheme': 'post-release'},
#             'setup_requires': [
#                 'setuptools_scm',
#                 'importlib-metadata>=0.12;python_version<"3.8"'],
#             }

setup(name='aiWT',
      description=description,
      long_description=long_description,
      url='',
      author=__author__,
      author_email=__contact__,
      license=__license__,
      **VERSION,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Topic :: Scientific/Engineering :: Chemistry',
          'Topic :: Scientific/Engineering :: Physics'
      ],
      packages=find_packages('src'),
      package_dir={'':'src'},
      include_package_data=True,
      install_requires= parse_requirements())
