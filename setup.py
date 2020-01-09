#!/usr/bin/env python

import os
from setuptools import setup
from buster import _version


setup(name="buster",
      version=_version.__version__,
      description="Static site generator for Ghost and Github",
      long_description=open("README.rst").read(),
      author="Akshit Khurana, Michael Zhuang",
      author_email="axitkhurana@gmail.com",
      url="https://github.com/axitkhurana/buster",
      license="MIT",
      packages=["buster"],
      entry_points={"console_scripts": ["buster = buster.buster:main"]},
      install_requires=['GitPython==0.3.5', 'async==0.6.2', 'docopt==0.6.2', 'gitdb==0.6.4', 'pyquery==1.4.1', 'smmap==0.9.0']
    )
