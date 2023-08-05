#!/usr/bin/env python

from setuptools import setup

setup(name = "mecab-python",
      description = "Redirect to mecab-python3",
      long_description = "Use mecab-python3 instead.",
      long_description_content_type = "text/markdown",
      maintainer = "Paul O'Leary McCann",
      maintainer_email = "polm@dampfkraft.com",
      url = "https://github.com/SamuraiT/mecab-python3",
      version='1.0.0rc1',
      setup_requires=['mecab-python3'],
      )
