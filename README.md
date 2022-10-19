# Python Onboarding Guide

Mini blog to myself about the technical steps to get a python development environment setup.

<!--TOC-->

- [Python Onboarding Guide](#python-onboarding-guide)
- [PyEnv](#pyenv)
  - [Install / Update](#install--update)
  - [Activate on demand](#activate-on-demand)
  - [List Versions you **CAN** install](#list-versions-you-can-install)
  - [List Versions that **ARE** installed](#list-versions-that-are-installed)
  - [Check and Activate a Version](#check-and-activate-a-version)
  - [Troubleshooting](#troubleshooting)
  - [Resources](#resources)
- [Poetry](#poetry)
  - [Install / Upgrade](#install--upgrade)
  - [Configuration](#configuration)
  - [Troubleshooting](#troubleshooting-1)
- [Invoke Common Tasks](#invoke-common-tasks)
  - [Install / Upgrade](#install--upgrade-1)
  - [Configuration](#configuration-1)
  - [Getting Help](#getting-help)

<!--TOC-->

# PyEnv

## Install / Update

```sh
brew update
brew install pyenv
```

> **DO NOT ENABLE PYENV BY DEFAULT**
>
> Do not install it to your `.zshrc` or `.bashrc`

## Activate on demand 

This causes the least magic 🔮 and you have better control over what is activated and when.
```sh
eval "$(pyenv init --path)"
```

## List Versions you **CAN** install

```sh
pyenv install --list | grep "  3\.9"

  3.9.0
  3.9-dev
  ...
  3.9.14
```

## List Versions that **ARE** installed

```sh
pyenv versions                      

  system
  2.7.18
  3.6.15
  3.7.13
* 3.8.12 (set by /Users/joshpeak/.pyenv/version)
  3.8.13
  3.9.10
  3.10.3
```

## Check and Activate a Version

Checking currently activated version
```sh
pyenv version

3.8.12 (set by /Users/joshpeak/.pyenv/version)
```

Activating a new globally set version
```sh
pyenv global 3.10.3

pyenv version      

3.10.3 (set by /Users/joshpeak/.pyenv/version)
```

## Troubleshooting

1. Always use `python3` and not `python`. This could resolve to a python2 installation.
1. Use `which -a python3` to figure out ALL `python3` binaries that could resolve from `PATH` environment variables and in which order.
    ```sh
    which -a python3  
    /Users/joshpeak/play/python-onboarding-guide/.venv/bin/python3
    /opt/homebrew/bin/python3
    /usr/bin/python3
    /opt/homebrew/bin/python3
    ```
1. When `deactivate`ing a poetry shell sometimes you need to `unset POETRY_ACTIVE` to clean the environment variables.
1. Use `python3 -m site` to triage if a library is not importing correctly. This lists the exact paths an `import` will traverse. It always has the *current directory* first, then *system libraries* that the virtual env links to and shares, and finally the locally installed libraries in your `.venv` 
    ```sh
    sys.path = [
        '/Users/joshpeak/play/python-onboarding-guide',
        '/opt/homebrew/Cellar/.../3.10/lib/python310.zip',
        '/opt/homebrew/Cellar/.../3.10/lib/python3.10',
        '/opt/homebrew/Cellar/.../3.10/lib/python3.10/lib-dynload',
        '/Users/joshpeak/play/python-onboarding-guide/.venv/lib/python3.10/site-packages',
    ]
    USER_BASE: '/Users/joshpeak/Library/Python/3.10' (doesn't exist)
    USER_SITE: '/Users/joshpeak/Library/Python/3.10/lib/python/site-packages' (doesn't exist)
    ENABLE_USER_SITE: False
    ```


## Resources
 - https://github.com/pyenv/pyenv
 - https://realpython.com/intro-to-pyenv/


---
# Poetry

Assuming you have a python environment setup from above, you will need to install `poetry` into that python installation to kick things off.

## Install / Upgrade

```sh
python3 -m pip install --upgrade pip poetry
# OR
python3 -m pip install -U pip poetry
```

## Configuration

You definitely want to create virtual environments only in the same folder as your project.

```sh
poetry config virtualenvs.in-project true --local
```

## Troubleshooting

99% of problems are resolved by resetting a borked virtual environment.

```sh
rm -rf .venv && rm poetry.lock
```

Then:

```sh
poetry lock && poetry install
```

---
# Invoke Common Tasks

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