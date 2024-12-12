# /// script
# dependencies = [
# ]
# ///
# https://docs.astral.sh/uv/guides/scripts/#creating-a-python-script
# https://packaging.python.org/en/latest/specifications/inline-script-metadata/#inline-script-metadata
#
# USAGE: python3 exportenv.py [--debug] [--unset]
# Load a .env file from the current working directory and print out the environment variables as export statements
#   --unset     print out unset statements instead
#   --debug     print out debugging statements as hash comments
#
# Use in combination with `eval $(python3 exportenv.py)` to load the environment variables into the current shell.
#
# One liner:
#
# curl -fsSL https://raw.githubusercontent.com/neozenith/python-onboarding-guide/refs/heads/main/scripts/exportenv.py | python3
#
# eval "$(curl -fsSL https://raw.githubusercontent.com/neozenith/python-onboarding-guide/refs/heads/main/scripts/exportenv.py | python3)"
#
# Using the extra args:
# curl -fsSL https://raw.githubusercontent.com/neozenith/python-onboarding-guide/refs/heads/main/scripts/exportenv.py | sh -c 'python3 - --debug'
# curl -fsSL https://raw.githubusercontent.com/neozenith/python-onboarding-guide/refs/heads/main/scripts/exportenv.py | sh -c 'python3 - --unset'
# curl -fsSL https://raw.githubusercontent.com/neozenith/python-onboarding-guide/refs/heads/main/scripts/exportenv.py | sh -c 'python3 - --debug --unset'
#
import logging
import pathlib
import sys

log = logging.getLogger(__name__)

log_level = logging.DEBUG if "--debug" in sys.argv else logging.INFO
logging.basicConfig(level=log_level, format='%(message)s')

log.debug(f"# {sys.argv}")
log.debug(f"# {pathlib.Path.cwd()}")

should_unset = "--unset" in sys.argv

env_file = pathlib.Path.cwd() / '.env'

if env_file.exists():
    with env_file.open() as f:
        for line in f:

            if not line.strip() or line.strip().startswith('#'):
                continue

            key, value = line.strip().split('=', 1)
            if should_unset:
                log.info(f'unset {key}')
            else:
                log.info(f'export {key}={value}')
