# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "jinja2",
#   "PyYAML",
#   "types-PyYAML"
# ]
# ///
# https://docs.astral.sh/uv/guides/scripts/#creating-a-python-script
# https://packaging.python.org/en/latest/specifications/inline-script-metadata/#inline-script-metadata
#
# Inspired by: https://github.com/neozenith/invoke-databricks-wheel-tasks/blob/main/invoke_databricks_wheel_tasks/tasks.py#L81
# Ultra flexible config templating system.
#
# Literally ANY config schema in a file format YML, JSON or TOML can be treated as a Jinja2 Template itself.
#
# This makes for VERY dynamic config.
# Then that config IS the config provided for a target template.
# This final template could be terraform, SQL, js, python or even more JSON or YAML.
#
# Output defaults to stdout or an output file can be specified.
#
# This allows some "ahead-of-time config" and some "just-in-time config" to all be injected into a final output.
# Absence of the "just-in-time" config results in merely merging the config file into the template.
#
# Templating variables and not providing a value will throw an error to ensure templating is correct at runtime.
#
# USAGE: python3 injinja.py [--debug] [--template/-t TEMPLATE]  [--config/-c CONFIGFILE] [--env KEY=VALUE] [--env KEY=VALUE] [--output OUTPUTFILE]
#
# One liner:
#
# curl -fsSL https://raw.githubusercontent.com/neozenith/python-onboarding-guide/refs/heads/main/scripts/injinja.py | sh -c "python3 - -t template.j2 -c config.yml -e home_dir=$HOME"
#

import argparse
import json
import logging
import pathlib
import sys
import tomllib
from typing import Any

import jinja2
import yaml

log = logging.getLogger(__name__)

log_level = logging.DEBUG if "--debug" in sys.argv else logging.INFO
logging.basicConfig(level=log_level, format='%(message)s')
log.debug(f"# {sys.argv}")
log.debug(f"# {pathlib.Path.cwd()}")

cli_config = {
    "debug": True,
    "template": {"required": True, "help": "The Jinja2 template file to use."},
    "config": {"required": True, "help": "The configuration file to use."},
    "env": {"action": "append", "default": [], "help": "Environment variables to pass to the template."},
    "output": "stdout"
}

def dict_from_keyvalue_list(args: list[str] | None = None) -> dict[str, str] | None:
    """Convert a list of 'key=value' strings into a dictionary."""
    return {k: v for k, v in [x.split("=") for x in args]} if args else None

def merge_template(template_filename: str, config: dict[str, Any] | None) -> str:
    """Load a Jinja2 template from file and merge configuration."""
    # Step 1: get raw content as a string
    raw_content = pathlib.Path(template_filename).read_text()

    # Step 2: Treat raw_content as a Jinja2 template if providing configuration
    if config:

        # NOTE: Providing jinja 2.11.x compatable version to better cross operate
        # with dbt-databricks v1.2.2 and down stream dbt-spark and dbt-core
        if int(jinja2.__version__[0]) >= 3:
            content = jinja2.Template(raw_content, undefined=jinja2.StrictUndefined).render(**config)
        else:
            content = jinja2.Template(raw_content).render(**config)

    else:
        content = raw_content

    return content


def load_config(filename: str, environment_variables: dict[str, str] | None = None) -> Any:
    """Detect if file is JSON or YAML and return parsed datastructure.

    When environment_variables is provided, then the file is first treated as a Jinja2 template.
    """
    # Step 1 & 2: Get raw template string and merge config (as necessary), returning as string
    content = merge_template(filename, environment_variables)

    # Step 3: Parse populated string into a data structure.
    if filename.lower().endswith("json"):
        return json.loads(content)
    elif any([filename.lower().endswith(ext) for ext in ["yml", "yaml"]]):
        return yaml.safe_load(content)
    elif filename.lower().endswith("toml"):
        return tomllib.loads(content)

    raise ValueError(f"File type of {filename} not supported.")  # pragma: no cover

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
        elif isinstance(flag_kwargs, bool):
            store_type = "store_true" if flag_kwargs else "store_false"
            parser.add_argument(short_flag, long_flag, action=store_type)
        else:
            parser.add_argument(short_flag, long_flag, default=flag_kwargs)
    return parser


def __handle_args(config, args):
    script_filename = pathlib.Path(__file__).name
    log.info(script_filename)
    if script_filename in args:
        args.remove(script_filename)
    return vars(__argparse_factory(config).parse_args(args))
    

def main(args):
  args = __handle_args(cli_config, sys.argv)
  env = dict_from_keyvalue_list(args['env'])
  conf = load_config(args['config'], env)
  merged_template = merge_template(args['template'], conf)
  
  if args['output'] == 'stdout':
    print(merged_template)
  else:
    pathlib.Path(args['output']).write_text(merged_template)
  

if __name__ == '__main__':
  main(sys.argv)
