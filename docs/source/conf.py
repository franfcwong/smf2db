# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import pathlib
import sys

_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
print(f"Root dir: {os.fspath(_ROOT)}")
sys.path.append(os.fspath(f"{_ROOT}/smf2db"))

project = 'smf2db'
copyright = '2026, Fran Wong'
author = 'Fran Wong'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

root_doc = "index"

extensions = [
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx_copybutton',
    'sphinx-jsonschema',
    'sphinx_design',
    'sphinx_sqlalchemy',
    'sphinx_toolbox.collapse',
]

nitpicky = True
nitpick_ignore = [
    ("envvar", "PATH"),
    ("py:func", "find_packages"),
    ("py:func", "setup"),
    ("py:func", "importlib.metadata.entry_points"),
    ("py:class", "importlib.metadata.EntryPoint"),
    ("py:func", "setuptools.find_namespace_packages"),
    ("py:func", "setuptools.find_packages"),
    ("py:func", "setuptools.setup"),
]

default_role = "any"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for internationalization --------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-internationalization

language = "en"

locale_dirs = ["../locales"]

gettext_auto_build = True
gettext_compact = "messages"
gettext_location = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_title = "smf2db User Guide"
html_theme = 'furo'

html_favicon = "assets/logo.png"
html_last_updated_fmt = ""
