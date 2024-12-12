# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "jinja2",
#   "PyYAML"
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
# This final template could be SQL, js, python or even more JSON or YAML.
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

import jinja2
import tomllib
import logging
import pathlib
import sys
import pyyaml as yaml

log = logging.getLogger(__name__)

log_level = logging.DEBUG if "--debug" in sys.argv else logging.INFO
logging.basicConfig(level=log_level, format='%(message)s')
log.debug(f"# {sys.argv}")
log.debug(f"# {pathlib.Path.cwd()}")

def dict_from_keyvalue_list(args: Optional[List[str]] = None) -> Optional[Dict[str, str]]:
    """Convert a list of 'key=value' strings into a dictionary."""
    return {k: v for k, v in [x.split("=") for x in args]} if args else None

def merge_template(template_filename: str, config: Optional[Dict[str, Any]]) -> str:
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


def load_config(filename: str, environment_variables: Optional[Dict[str, str]] = None) -> Any:
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

def main(args):
  log.info('main...')
  # TODO: Handle CLI args
  # env = dict_from_keyvalue_list(environment_variable)
  env = {}
  # conf = load_config(config_file, env)
  # merged_template = merge_template(jinja_template, conf)
  log.info(merged_template)

if __name__ == '__main__':
  main(sys.argv)
