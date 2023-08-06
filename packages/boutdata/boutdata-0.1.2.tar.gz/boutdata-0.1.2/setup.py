#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import setuptools
from pathlib import Path

name = 'boutdata'
root_path = Path(__file__).parent
init_path = root_path.joinpath(name, '__init__.py')
readme_path = root_path.joinpath('README.md')

# https://packaging.python.org/guides/single-sourcing-package-version/
with init_path.open('r') as f:
    version_file = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError('Unable to find version string.')

with readme_path.open('r') as f:
    long_description = f.read()

setuptools.setup(
    name=name,
    version=version,
    author='Ben Dudson et al.',
    description='Python package for collecting BOUT++ data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://boutproject.github.io',
    project_urls={
        "Bug Tracker": "https://github.com/boutproject/boutdata/issues/",
        "Documentation": "http://bout-dev.readthedocs.io/en/latest/",
        "Source Code": "https://github.com/boutproject/boutdata/",
    },
    packages=setuptools.find_packages(),
    keywords=['bout++',
              'bout',
              'plasma',
              'physics',
              'data-extraction',
              'data-analysis',
              'data-visualization'],
    install_requires=['sympy',
                      'numpy',
                      'matplotlib',
                      'scipy',
                      'bunch',
                      'boututils'],
    classifiers=[
        'Programming Language :: Python :: 3',
        ('License :: OSI Approved :: '
         'GNU Lesser General Public License v3 or later (LGPLv3+)'),
        'Operating System :: OS Independent',
    ],
)
