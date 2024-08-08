# PyEnv

<!--TOC-->

- [PyEnv](#pyenv)
  - [Install / Update](#install--update)
  - [Activate on demand](#activate-on-demand)
    - [Avoiding magic](#avoiding-magic)
  - [List Versions you **CAN** install](#list-versions-you-can-install)
  - [List Versions that **ARE** installed](#list-versions-that-are-installed)
  - [Check and Activate a Version](#check-and-activate-a-version)
  - [PyEnv Troubleshooting](#pyenv-troubleshooting)
  - [Resources](#resources)

<!--TOC-->

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

