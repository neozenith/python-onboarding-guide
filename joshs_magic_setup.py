"""
Josh Peak's Opinionated Python setup.
If you are using this... why? I made it for me.

It's ok, you can steal it. I won't tell anyone ;)
"""

import argparse
import sys
from urllib.request import Request, urlopen
import ssl
from pathlib import Path

cli_config = {
    "overwrite": {"help": "Overwrite existing files", "action": "store_true"},
    "target-path": {"help": "Path to download files to", "default": "."},
}

raw_file_host = (
    "https://raw.githubusercontent.com/neozenith/python-onboarding-guide/main/"
)

extra_files = ["Makefile", ".pre-commit-config.yaml", ".flake8", "pyproject.toml"]


def download_file(url, local_file_path, overwrite=False):
    # Download the file from `url` and save it locally under `local_file_path`
    ssl_context = ssl.create_default_context()
    print(url)

    output_file = Path(local_file_path)
    if output_file.exists() and not overwrite:
        print(f"File {local_file_path} already exists. Skipping download.")
        return

    req = Request(url, method="GET", data=None)
    with urlopen(req, context=ssl_context) as response:
        output_file.write_bytes(response.read())


def __argparse_factory(config):
    """Josh's Opinionated Argument Parser Factory."""
    parser = argparse.ArgumentParser()

    # Take a dictionary of configuration. The key is the flag name, the value is a dictionary of kwargs.
    for flag, flag_kwargs in config.items():
        # Automatically handle long and short case for flags
        lowered_flag = flag.lower()
        short_flag = f"-{lowered_flag[0]}"
        long_flag = f"--{lowered_flag}"

        # If the value of the config dict is a dictionary then unpack it like standard kwargs for add_argument
        # Otherwise assume the value is a simple default value like a string.
        if isinstance(flag_kwargs, dict):
            parser.add_argument(short_flag, long_flag, **flag_kwargs)
        else:
            parser.add_argument(short_flag, long_flag, default=flag_kwargs)
    return parser


def __handle_args(config, args):
    parser = __argparse_factory(config)
    return vars(parser.parse_args(args))


if __name__ == "__main__":
    args = __handle_args(cli_config, sys.argv[1:])
    print(args)
    target_path = Path(args["target_path"])
    for f in extra_files:
        download_file(
            f"{raw_file_host}{f}", target_path / f, overwrite=args["overwrite"]
        )
    # TODO:
    # Create folder structures
    # Create config files
    # Copy scripts
