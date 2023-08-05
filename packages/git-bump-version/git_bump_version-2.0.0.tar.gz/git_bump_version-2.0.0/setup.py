#!/usr/bin/env python3
import sys
from setuptools import setup

setup(
  name = 'git_bump_version',
  packages = ['git_bump_version'], # this must be the same as the name above
  use_scm_version = True,
  description = 'Automatically bumps version based on last tag and current branch',
  author = 'Nathan Grubb',
  author_email = 'mrnathangrubb@gmail.com',
  url = 'https://github.com/silent-snowman/git_bump_version',
  keywords = ['git', 'tag', 'version'],
  setup_requires=[
    'setuptools_scm',
  ],
  entry_points={
    'console_scripts' : [
      'git_bump_version = git_bump_version.__init__:main'
    ]},
  install_requires=[
    'GitPython',
  ],
)
