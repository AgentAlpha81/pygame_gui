# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import sphinx_rtd_theme


sys.path.insert(0, os.path.abspath('../../'))
sys.path.insert(0, os.path.abspath('../../pygame_gui/'))
sys.path.insert(0, os.path.abspath('../../pygame_gui/windows/'))
sys.path.insert(0, os.path.abspath('../../pygame_gui/elements/'))
sys.path.insert(0, os.path.abspath('../../pygame_gui/core/'))
sys.path.insert(0, os.path.abspath('../../pygame_gui/core/drawable_shapes/'))
sys.path.insert(0, os.path.abspath('../../pygame_gui/core/interfaces/'))
sys.path.insert(0, os.path.abspath('../../pygame_gui/core/text/'))


# -- Project information -----------------------------------------------------

project = 'Pygame GUI'
copyright = '2019, Dan Lawrence'
author = 'Dan Lawrence'

# The short X.Y version
version = '0.6.11'
# The full version, including alpha/beta/rc tags
release = '0.6.11'


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.ifconfig',
    'sphinx_rtd_theme',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source file names.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_logo = '_static/pygame_gui_logo.png'
html_theme_options = {'logo_only': True}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'pygame_gui_doc'
smartquotes = False

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

autodoc_mock_imports = ["ctypes"]
