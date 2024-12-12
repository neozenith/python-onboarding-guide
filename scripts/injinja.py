# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "jinja2",
# ]
# ///
# https://docs.astral.sh/uv/guides/scripts/#creating-a-python-script
# https://packaging.python.org/en/latest/specifications/inline-script-metadata/#inline-script-metadata
#
# USAGE: python3 injinja.py [--output OUTPUTFILE] [--input INPUTFILE]
#
# One liner:
#
# curl -fsSL https://raw.githubusercontent.com/neozenith/python-onboarding-guide/refs/heads/main/scripts/injinja.py | python3
#
# eval "$(curl -fsSL https://raw.githubusercontent.com/neozenith/python-onboarding-guide/refs/heads/main/scripts/injinja.py | python3)"
#
import jinja2
import logging
import pathlib
import sys

log = logging.getLogger(__name__)

log_level = logging.DEBUG if "--debug" in sys.argv else logging.INFO
logging.basicConfig(level=log_level, format='%(message)s')

log.debug(f"# {sys.argv}")
log.debug(f"# {pathlib.Path.cwd()}")
