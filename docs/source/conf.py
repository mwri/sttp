"""Sphinx docs config."""

import os
import sys

sys.path.append(os.path.realpath(os.path.dirname(os.path.abspath(__file__)) + '/../..'))

import sttp


project = 'STTP'
copyright = '2021, ' + sttp.pkg_meta.author
author = sttp.pkg_meta.author
release = sttp.pkg_meta.version
version = sttp.pkg_meta.version

extensions = [
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.doctest',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
