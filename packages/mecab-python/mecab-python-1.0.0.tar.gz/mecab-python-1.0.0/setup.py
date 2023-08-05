#!/usr/bin/env python

from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name = "mecab-python",
      description = "Redirect to mecab-python3",
      long_description = long_description,
      long_description_content_type = "text/markdown",
      maintainer = "Paul O'Leary McCann",
      maintainer_email = "polm@dampfkraft.com",
      url = "https://github.com/SamuraiT/mecab-python3",
      version='1.0.0',
      install_requires=['mecab-python3'],
      )
