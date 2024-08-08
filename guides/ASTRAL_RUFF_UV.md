# Astral Tool Chain

<!--TOC-->

- [Astral Tool Chain](#astral-tool-chain)
  - [Precommit setup](#precommit-setup)
  - [Installing Precommit and Astral tool chain](#installing-precommit-and-astral-tool-chain)

<!--TOC-->

[https://astral.sh/](https://astral.sh/) are the makers of:

- [`ruff`](https://astral.sh/ruff)
    - drop in replacements for a bunch of Python linting and formatting tools but rewritten in Rust.
- [`uv`](https://github.com/astral-sh/uv)
    - drop in replacement for `pip` and `piptools`

This section needs to get fleshed out better.


## Precommit setup

`.pre-commit-config.yml`

```yml
repos:
- repo: https://github.com/astral-sh/ruff-pre-commit
  # Ruff version.
  rev: v0.4.4
  hooks:
    # Run the formatter.
    - id: ruff-format
      types_or: [ python, pyi, jupyter ]
    # Run the linter.
    - id: ruff
      types_or: [ python, pyi, jupyter ]
      args: [ --fix ]
```
    
## Installing Precommit and Astral tool chain

Example `Makefile` steps:


```Makefile
# Depends if the virtual environment has been setup
init: .venv/bin/python3

# The output of this step is ensuring the virtual environment is setup correctly
# It is here we guarantee uv and pre-commit get installed.
.venv/bin/python3:
	[ ! -d ".venv" ] && python3 -m venv .venv || echo ".venv already setup"
	.venv/bin/python3 -m pip install -qq --upgrade pip uv wheel pre-commit
	.venv/bin/pre-commit install
```
