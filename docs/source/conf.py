# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
# At the top.
import os
import sys

sys.path.insert(
    0, os.path.abspath("../../src/dswb/")
)  # Source code dir relative to this file
# ...


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Data Science Workbench"
copyright = "2024, Duck Bongos"
author = "Duck Bongos"
# release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
extensions = [
    "autoapi.extension",
]

autoapi_dirs = ["../../src/dswb"]
autoapi_type = "python"
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]
autoapi_keep_files = True
# autodoc_typehints = "signature"

napoleon_google_docstring = True

templates_path = ["_templates"]
exclude_patterns = ["_build", "_templates"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
# Activate the theme.
html_theme = "furo"
html_logo = "../img/source_img/human_logo.png"  # relative to _static
html_static_path = ["_static"]
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#0a4bff",
        "color-brand-content": "#02694c",
        "color-brand-visited": "#0a4bff",
        # "color-background-secondary": "#02694c",
        "color-api-name": "#02694c",
    },
    "dark_css_variables": {
        "color-brand-primary": "#02694c",
        "color-brand-content": "#eea051",
        "color-brand-visited": "#fefefe",
        "color-api-name": "#51ee51",
        "color-api-pre-name": "#eea051",
    },
}


# html_theme_options = {
#     "light_css_variables": {
#         "color-brand-primary": "#ecf4f4",
#         "color-brand-content": "#02694c",
#     },
#
# }


def skip_member(app, what, name, obj, skip, options):
    # skip submodules
    if what == "module":
        skip = True
    return skip


def setup(sphinx):
    sphinx.connect("autoapi-skip-member", skip_member)


source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "restructuredtext",
    ".md": "markdown",
}
