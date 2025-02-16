# ruff: noqa: E501
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
# eval "$(curl -fsSL https://raw.githubusercontent.com/neozenith/python-onboarding-guide/refs/heads/main/scripts/exportenv.py | python3)"
#
# Using the extra args:
# curl -fsSL https://raw.githubusercontent.com/neozenith/python-onboarding-guide/refs/heads/main/scripts/exportenv.py | sh -c 'python3 - --debug'
# curl -fsSL https://raw.githubusercontent.com/neozenith/python-onboarding-guide/refs/heads/main/scripts/exportenv.py | sh -c 'python3 - --unset'
# curl -fsSL https://raw.githubusercontent.com/neozenith/python-onboarding-guide/refs/heads/main/scripts/exportenv.py | sh -c 'python3 - --debug --unset'
#
# Standard Library
import logging
import pathlib
import sys
import shlex

log = logging.getLogger(__name__)

log_level = logging.DEBUG if "--debug" in sys.argv else logging.INFO


def __parse_env_line(line: str) -> tuple[str | None, str | None]:
    """Parses a single line into a key-value pair. Handles quoted values and inline comments.
    Returns (None, None) for invalid lines."""
    # Guard checks for empty lines or lines without '='
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        return None, None

    # Split the line into key and value at the first '='
    key, value = line.split("=", 1)
    key = key.strip()

    # Use shlex to process the value (handles quotes and comments)
    lexer = shlex.shlex(value, posix=True)
    lexer.whitespace_split = True  # Tokenize by whitespace
    value = "".join(lexer)  # Preserve the full quoted/cleaned value

    return key, value


def read_env_file(file_path: str | pathlib.Path) -> dict[str, str] | None:
    """Reads a .env file and returns a dictionary of key-value pairs.
    If the file does not exist or is not a regular file, returns None.
    """
    file = filepath if type(file_path) == pathlib.Path else pathlib.Path(file_path)
    return (
        {
            key: value
            for key, value in map(__parse_env_line, file.read_text().splitlines())
            if key is not None and value is not None
        }
        if file.is_file()
        else None
    )

def main(should_unset: bool = False):
    env_file = pathlib.Path.cwd() / ".env"
    if env_file.exists():
        env_values = read_env_file(env_file)

        for key, value in env_values.items():
            if should_unset:
                log.info(f"unset {key}")
            else:
                log.info(f"export {key}={value}")


if __name__ == "__main__":
    logging.basicConfig(level=log_level, format="%(message)s")

    log.debug(f"# {sys.argv}")
    log.debug(f"# {pathlib.Path.cwd()}")
    should_unset = "--unset" in sys.argv
    main(should_unset)

    

