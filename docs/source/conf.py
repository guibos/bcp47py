# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys


def add_to_path():

    partial_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../../src/bcp47py')
    workspace_path = os.path.abspath(partial_path)
    assert os.path.exists(workspace_path)

    projects = []

    for current, dirs, c in os.walk(str(workspace_path)):
        for dir in dirs:

            project_path = os.path.join(workspace_path, dir, 'src')

            if os.path.exists(project_path):
                projects.append(project_path)

    for project_str in projects:
        sys.path.append(project_str)


add_to_path()

project = 'BCP47Py'
copyright = '2023, Guillermo Ferrer Bosque'
author = 'Guillermo Ferrer Bosque'
release = 'Mozilla Public License Version 2.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

autodoc_default_options = {
    'members': True,
    # Does now show base classes otherwise... why such bad defaults?
    # But with this it does show useless bases like `object`. What is one to do?
    'show-inheritance': True,
}

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

