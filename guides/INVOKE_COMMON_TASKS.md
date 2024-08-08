# Invoke Common Tasks

<!--TOC-->

- [Invoke Common Tasks](#invoke-common-tasks)
  - [Install / Upgrade](#install--upgrade)
  - [Configuration](#configuration)
  - [Getting Help](#getting-help)

<!--TOC-->

This is a package I developed and have kind of abandonded as I have moved on to classic `Makefile`s. 

Thanks to Windows Subsystem for Linux (WSL2) and even Git Bash for Windows there is always a POSIX compatable version of `make` floating around and it is on macOS too.

## Install / Upgrade

```sh
poetry add --group dev 'invoke-common-tasks[all]' invoke
```

## Configuration

Create a `tasks.py` file with:

```python
from invoke_common_tasks import * # noqa
```

Then run:

```sh
poetry run invoke init-config --all

Initialise config options selected:
format:    True
lint:      True
typecheck: True
test:      True
Adding format config...
Adding linting config...
Adding typecheck config...
Adding test config...
Saving updated config...
```

## Getting Help

```sh
poetry run invoke --list

Available tasks:

  build         Build wheel.
  ci            Run linting and test suite for Continuous Integration.
  format        Autoformat code for code style.
  init-config   Setup default configuration for development tooling.
  lint          Linting and style checking.
  test          Run test suite.
  typecheck     Run typechecking tooling.
```

or add `--help` to any command.

For example:
```sh
invoke init-config --help

Usage: inv[oke] [--core-opts] init-config [--options] [other tasks here ...]

Docstring:
  Setup default configuration for development tooling.

Options:
  -a, --all
  -f, --format
  -l, --lint
  -t, --test
  -y, --typecheck
```
