# ruff: noqa: E501
# /// script
# requires-python = ">=3.11"
# dependencies = [
# "ruamel.yaml",
# ]
# ///
# https://docs.astral.sh/uv/guides/scripts/#creating-a-python-script
# https://packaging.python.org/en/latest/specifications/inline-script-metadata/#inline-script-metadata
#
# USAGE:
# curl -fsSL https://raw.githubusercontent.com/neozenith/python-onboarding-guide/refs/heads/main/scripts/yaml-check.py | sh -c 'python3 - path/to/yamlfile.yml'

#
import ruamel.yaml
from pprint import pprint as pp
import sys
from pathlib import Path
import logging
import json
log = logging.getLogger(__name__)


def preview_yaml(filepath: str):
    """Read and preview a YAML file."""
    p = Path(filepath)
    yaml = ruamel.yaml.YAML()
    yaml.preserve_quotes = True
    yaml.sort_keys = False
    yaml.indent(mapping=2, sequence=4, offset=2)
    content = yaml.load(p.read_text(encoding="utf-8"))
    log.info("Content:")
    print(json.dumps(content, indent=2))
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) != 2:
        print("Usage: preview_yaml.py <path_to_yaml>")
        sys.exit(1)
    
    preview_yaml(sys.argv[1])
