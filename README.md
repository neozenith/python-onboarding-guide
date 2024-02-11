# Python Onboarding Guide

Mini blog to myself about the technical steps to get a python development environment setup.

<!--TOC-->

- [Python Onboarding Guide](#python-onboarding-guide)
- [PyEnv](#pyenv)
  - [Install / Update](#install--update)
  - [Activate on demand](#activate-on-demand)
    - [Avoiding magic](#avoiding-magic)
  - [List Versions you **CAN** install](#list-versions-you-can-install)
  - [List Versions that **ARE** installed](#list-versions-that-are-installed)
  - [Check and Activate a Version](#check-and-activate-a-version)
  - [PyEnv Troubleshooting](#pyenv-troubleshooting)
  - [Resources](#resources)
- [Pip & pip-tools](#pip--pip-tools)
  - [pip-tools quickstart](#pip-tools-quickstart)
- [Poetry](#poetry)
  - [Install / Upgrade](#install--upgrade)
  - [Configuration](#configuration)
  - [Poetry Troubleshooting](#poetry-troubleshooting)
- [Invoke Common Tasks](#invoke-common-tasks)
  - [Install / Upgrade](#install--upgrade-1)
  - [Configuration](#configuration-1)
  - [Getting Help](#getting-help)
- [Typechecking](#typechecking)
  - [Level 1 - Opting In](#level-1---opting-in)
    - [😎 This works](#-this-works)
    - [😰 This does not work](#-this-does-not-work)
  - [Level 2 - Minimal Enforcement](#level-2---minimal-enforcement)
    - [😎 This works](#-this-works-1)
    - [😰 This does not work](#-this-does-not-work-1)
  - [Level 3 - Strict](#level-3---strict)
  - [Further Reading](#further-reading)
- [Documentation - MKDocs](#documentation---mkdocs)

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

This causes the least magic 🔮* and you have better control over what is activated and when.
```sh
eval "$(pyenv init --path)"
```

### Avoiding magic

<details>
  <summary>Click here for a deeper dive into avoiding *magic 🔮 </summary>

[![The Python environmental protection agency wants to seal it in a cement chamber, with pictorial messages to future civilizations warning them about the danger of using sudo to install random Python packages.](assets/xkcd_1987_python_environment_2x.png)](https://xkcd.com/1987/)

> __*magic 🔮__ --> refers to `pip install poetry` or `pip install awscli` could resolve to installing it into **ANY** of **MANY** different python versions that might exist on your `PATH` and this all depends on the order they resolve.
>
> So when trying to upgrade it can get problematic...
>
> For example you install `poetry` into `homebrew/python3.8` but then `homebrew upgrade python3` and that now resolves to `hombrew/python3.9`.
> `poetry` is still resolving first on `PATH` but `pip install --upgrade poetry` is pointing to `homebrew/python3.9`.
>
> The main way to avoid this completely and over the top is to use the `python3 -m pip install --upgrade poetry` format of the command, but use the absolute path to the version of python you need like:
> ```sh
>/opt/homebrew/bin/python3.8 -m pip install --upgrade poetry
> # OR
> $HOME/.pyenv/shims/python3.8 -m pip install --upgrade poetry
> ```
</details>


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

## PyEnv Troubleshooting

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
# Pip & pip-tools

> Work in Progress

Sometimes you can't use `poetry` or your environment is somewhat constrained to only `pip`. 
Or for better compatability when locking down your dependencies for Docker.
I'm using `pip-tools` here until I determine the pip only route to achieve the same thing.

## pip-tools quickstart

```sh
python3 -m venv .venv
. ./.venv/bin/activate

python3 -m pip install -U pip pip-tools
mkdir -p requirements src/myproject
touch src/myproject/__init__.py
```

https://www.b-list.org/weblog/2022/may/13/boring-python-dependencies/

`pyproject.toml`
```toml
[project]
name = "myproject"
description = ""
version = "0.1.0"
authors = []


[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
```

`requirements/app.in`
```
-e .
flask
```

Now generate the hashes...

```sh
python3 -m pip install --upgrade pip-tools
python3 -m piptools compile --generate-hashes requirements/app.in --output-file requirements/app.txt
```

`requirements/app.txt`
```
#
# This file is autogenerated by pip-compile with Python 3.10
# by the following command:
#
#    pip-compile --generate-hashes --output-file=requirements/app.txt requirements/app.in
#
-e file:///Users/username/path/to/project
    # via -r requirements/app.in
blinker==1.7.0 \
    --hash=sha256:c3f865d4d54db7abc53758a01601cf343fe55b84c1de4e3fa910e420b438d5b9 \
    --hash=sha256:e6820ff6fa4e4d1d8e2747c2283749c3f547e4fee112b98555cdcdae32996182
    # via flask
click==8.1.7 \
    --hash=sha256:ae74fb96c20a0277a1d615f1e4d73c8414f5a98db8b799a7931d1582f3390c28 \
    --hash=sha256:ca9853ad459e787e2192211578cc907e7594e294c7ccc834310722b41b9ca6de
    # via flask
.....
etc, etc, etc
```

https://www.b-list.org/weblog/2023/dec/07/pip-install-safely/

```sh
python -m pip install \
    --require-hashes \
    --no-deps \
    --only-binary :all: \
    -r requirements/app.txt
```



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

## Poetry Troubleshooting

1. 99% of problems are resolved by resetting a borked virtual environment.

```sh
rm -rf .venv && rm poetry.lock
```

Then:

```sh
poetry lock && poetry install
```

2. When `deactivate`ing a poetry shell sometimes you need to `unset POETRY_ACTIVE` to clean the environment variables.

3. Issues with `poetry` across multiple version of Python, `poetry` is installed _**per Python version**_. 
   
   Use the following when in doubt:
   ```sh
   python3 -m install -U poetry pip
   python3 -m poetry shell
   ```
   1. **The problem**: When I run `poetry` on the commandline it resolves based on my `PATH`
   2. So `python3 --version` could show `3.9`, but `poetry` is installed in my `3.8`
   3. `poetry` will create a virtual environment based on the `python3` interpreter that it is being run in.
   4. `python3 -m poetry` uses the exact version of `poetry` that is relative to the same `python3` you are expecting because you are using _module mode_ (`-m`).
   5. This is part of the reason you upgrade `pip` using `python3 -m pip install -U pip` to make sure you are updating the same `pip` as your target `python3` interpreter. 
   6. This is why I only activate `pyenv` on demand to have least magic on my `PATH` at any given time.

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

---
# Typechecking

As a Data / ML Engineer, a lot of my work is enforcing schemas and making sure data is correct. That is why typechecking is an invaluable tool for Data / ML Engineers as well as runtime checking tools like [`pydantic`](https://pydantic-docs.helpmanual.io/)

To incrementally adopt typehints in a project here are the three levels and the associated `pyproject.toml` configuration for [`mypy`](https://mypy.readthedocs.io/en/stable/).

The idea is that _in conversation with your team_, you add each level when the team is ready to adopt the increasing costs and strictness. An example timeline could be 3 months at each level.

1. The first level allows some typechecking for early adopters that start adding it to the code base but it is not enforced.
2. The second level does require some work, but should be a manageable amount to adopt by focusing on only functions and method signatures.
3. The last level is more detailed and requires more work, but the bulk of the work is covered in level 2.

## Level 1 - Opting In

The first level allows some typechecking for early adopters that start adding it to the code base but it is not enforced.

With the following settings:

```toml
[tool.mypy]
exclude = ["tests/", "tasks\\.py"]
pretty = true
show_error_codes = true
show_column_numbers = true
show_error_context = true
ignore_missing_imports = true
follow_imports = "silent"

# Level 1
disallow_incomplete_defs = true

# Level 2
disallow_untyped_defs = false

# Level 3
strict = false
```

### 😎 This works

Existing code with no typehints stays fine 👍

```python
def forecast(x, m = 1, b = 0):
  """Forecast using linear regression."""
  return m * x + b
```

Fully typed code works too 👍

```python
def forecast(x: float, m: float = 1, b: float = 0) -> float:
  """Forecast using linear regression."""
  return m * x + b
```

### 😰 This does not work

Partially typed code will not work

```python
def forecast(x: float, m = 1, b = 0) -> float: # Some arguments are not typed
  """Forecast using linear regression."""
  return m * x + b
```

```python
def forecast(x: float, m: float = 1, b: float = 0): # Missing Return type
  """Forecast using linear regression."""
  return m * x + b
```

## Level 2 - Minimal Enforcement

The second level does require some work, but should be a manageable amount to adopt by focusing on only functions and method signatures.

With the following settings:

```toml
[tool.mypy]
exclude = ["tests/", "tasks\\.py"]
pretty = true
show_error_codes = true
show_column_numbers = true
show_error_context = true
ignore_missing_imports = true
follow_imports = "silent"

# Level 1
disallow_incomplete_defs = true

# Level 2
disallow_untyped_defs = true

# Level 3
strict = false
```

### 😎 This works

Only fully typed functions and methods works  👍

```python
def forecast(x: float, m: float = 1, b: float = 0) -> float:
  """Forecast using linear regression."""
  return m * x + b
```

### 😰 This does not work

Untyped and partially typed code will not work

```python
def forecast(x, m = 1, b = 0):
  """Forecast using linear regression."""
  return m * x + b
```

```python
def forecast(x: float, m = 1, b = 0) -> float: # Some arguments are not typed
  """Forecast using linear regression."""
  return m * x + b
```

```python
def forecast(x: float, m: float = 1, b: float = 0): # Missing Return type
  """Forecast using linear regression."""
  return m * x + b
```

## Level 3 - Strict

The last level is more detailed and requires more work, but the bulk of the work is covered in level 2.

With the following settings:

```toml
[tool.mypy]
exclude = ["tests/", "tasks\\.py"]
pretty = true
show_error_codes = true
show_column_numbers = true
show_error_context = true
ignore_missing_imports = true
follow_imports = "silent"

# Level 1
disallow_incomplete_defs = true

# Level 2
disallow_untyped_defs = true

# Level 3
strict = true
```

For the full specific of `strict` then [MyPy Strict Options](https://mypy.readthedocs.io/en/stable/existing_code.html#introduce-stricter-options).

This pretty much disallows the use of `Any` amongst some other corner cases, but disallowing `Any` is a big one on the way to becoming a fully typed codebase.

## Further Reading

Checkout the [MyPy Existing Code Guide](https://mypy.readthedocs.io/en/stable/existing_code.html) for more details.

---
# Documentation - MKDocs

`requirements/docs.in`

```txt
# Bare minimum
mkdocs
mkdocs-material
mkdocstrings
mkdocstrings-python
mkdocs-gen-files
mkdocs-literate-nav
mkdocs-section-index
mkdocs-git-revision-date-localized-plugin
mkdocs-git-authors-plugin
mkdocs-render-swagger-plugin

# Scientific + Engineering
mkdocs-jupyter
mkdocs-plotly-plugin
mkdocs-blogging-plugin
mkdocs-drawio-exporter
```

`mkdocs.yaml`

```yaml
site_name: example-site-name
site_url: https://example-site-name.github.io/

theme:
  name: material

plugins:
- search  
- git-authors
- git-revision-date-localized

# Blogging
- blogging:
    dirs: # The directories to be included
      - blog

# Auto Documentation From Code      
- gen-files: # Generate distinct docs pages per source code file.
    scripts:
    - scripts/mkdocs/gen_ref_pages.py  
- literate-nav:
    nav_file: SUMMARY.md
- section-index
- mkdocstrings: # Generate documentation from source code.
    default_handler: python
    handlers:
      python:
        options:
          docstring_style: google
          docstring_section_style: list
          show_if_no_docstring: true
          show_submodules: true
          show_bases: true
          
          show_root_full_path: true
          show_object_full_path: false
          group_by_category: true
          show_category_heading: true
          show_source: false
          show_signature: true
          separate_signature: true
          show_signature_annotations: true

# Swagger OpenAPI doc generation
- render_swagger

# Science and Engineering
- plotly
- drawio-exporter
- mkdocs-jupyter

markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: plotly
          class: mkdocs-plotly
          format: !!python/name:mkdocs_plotly_plugin.fences.fence_plotly
nav:
- 'index.md'
- Code Reference: reference/  
```

`.readthedocs.yml`

```yml

# Read the Docs configuration file for MkDocs projects
# See https://docs.readthedocs.io/en/stable/config-file/v2.html for details

# Required
version: 2

# Set the version of Python and other tools you might need
build:
  os: ubuntu-22.04
  tools:
    python: "3.10"

mkdocs:
  configuration: mkdocs.yml

# Optionally declare the Python requirements required to build your docs
python:
  install:
  - requirements: docs/requirements.txt
```

`scripts/mkdocs/gen_ref_pages.py`

```python
"""Generate the code reference pages and navigation."""

# Standard Library
from pathlib import Path

# Third Party
import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

src = Path(__file__).parent.parent / "src"

for path in sorted(src.rglob("*.py")):
    module_path = path.relative_to(src).with_suffix("")
    doc_path = path.relative_to(src).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)

    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    nav[parts] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(parts)
        fd.write(f"::: {ident}")

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
```

`docs/index.md`

```md
# Index Heading

![Architecture](diagrams/architecture.drawio)
```