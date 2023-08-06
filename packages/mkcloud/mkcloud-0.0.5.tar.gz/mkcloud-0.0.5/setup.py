#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
  name="mkcloud",
  version="0.0.5",
  author="makeblock",
  author_email="developer@makeblock.com",
  description="a robot",
  long_description=long_description,
  long_description_content_type='text/markdown',
  url="https://github.com/pypa/mkcloud",    
  packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
  include_package_data=True,
  classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
  license='MIT',
  platforms=["all"],
  install_requires = ['requests'],
  python_requires='>=3.6.0',
)