# Poetry

<!--TOC-->

- [Poetry](#poetry)
  - [Install / Upgrade](#install--upgrade)
  - [Configuration](#configuration)
  - [Poetry Troubleshooting](#poetry-troubleshooting)

<!--TOC-->

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
