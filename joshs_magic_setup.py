"""
Josh Peak's Opinionated Python setup. 
If you are using this... why? I made it for me. 

It's ok, you can steal it. I won't tell anyone ;)
"""

from pathlib import Path
import argparse
import sys

cli_config = {
   "mkdocs": "all" # Options should be basic/blog/api/scientific/all
}

folder_structure = {
    "assets": {},
    "docs": {
        "blog",
        "notebooks",
        "diagrams",
        "index.md"
    },
    "requirements": {},
    "scripts": {
        "mkdocs": {
           "gen_ref_pages.py"
        }
    },
    
    ".readthedocs.yml": {},
    "mkdocs.yml": {},
    "pyproject.toml":{}
}

MKDOCS_REQUIREMENTS = """
# Bare minimum
mkdocs
mkdocs-material
mkdocstrings
mkdocstrings-python
mkdocs-gen-files
mkdocs-literate-nav
mkdocs-section-index
mkdocs-git-revision-date-localized-plugin
mkdocs-git-authors-plugin
mkdocs-render-swagger-plugin

# Scientific + Engineering
mkdocs-jupyter
mkdocs-plotly-plugin
mkdocs-blogging-plugin
mkdocs-drawio-exporter
"""


def __argparse_factory(config):
  parser = argparse.ArgumentParser()
  for flag, flag_kwargs in config.items():
    lowered_flag = flag.lower()
    short_flag = f"-{lowered_flag[0]}"
    long_flag = f"--{lowered_flag}"
    if type(flag_kwargs) == dict:
      parser.add_argument(short_flag, long_flag, **flag_kwargs)
    else:
      parser.add_argument(short_flag, long_flag, default=flag_kwargs)
  return parser

def __handle_args(config, args):
   parser = __argparse_factory(config)
   return vars(parser.parse_args(args))

def pyproject(project_name):
    return f"""
[project]
name = "{project_name}"
description = ""
version = "0.1.0"
authors = []


[tool.setuptools]
package-dir = {{"" = "src"}}

[tool.setuptools.packages.find]
where = ["src"]
"""

def readthedocs(python_version="3.10", mkdocs_config_path="mkdocs.yml", requirements_path="docs/requirements.txt"):
    return f"""
# Read the Docs configuration file for MkDocs projects
# See https://docs.readthedocs.io/en/stable/config-file/v2.html for details

# Required
version: 2

# Set the version of Python and other tools you might need
build:
  os: ubuntu-22.04
  tools:
    python: "{python_version}"

mkdocs:
  configuration: {mkdocs_config_path}

# Optionally declare the Python requirements required to build your docs
python:
  install:
  - requirements: {requirements_path}
"""

if __name__ == "__main__":
    print(__handle_args(cli_config, sys.argv[1:]))
    # TODO: 
    # Create folder structures
    # Create config files
    # Copy scripts