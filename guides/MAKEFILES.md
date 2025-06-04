# Makefiles

## .gitignore

```gitignore
.make
.venv
.*_cache
```

## Common Header Tasks

```makefile
# Ensure the .make folder exists when starting make
# We need this for build targets that have multiple or no file output.
# We 'touch' files in here to mark the last time the specific job completed.
_ := $(shell mkdir -p .make)
SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

# Derive the app name from the git remote repo name and not trust what the local folder name is.
# https://stackoverflow.com/a/42543006/622276
GIT_REMOTE_URL:=$(shell git config --get remote.origin.url)
PROJECT_NAME:=$(shell basename -s .git ${GIT_REMOTE_URL})
AWS_ACCOUNT_ID:=123456789012
AWS_REGION:=ap-southeast-2
AWS_PROFILE:=$(AWS_ACCOUNT_ID)_JPEAK

.PHONY: clean init plan apply

################################# MISC #################################

clean: # Clean derived artifacts as though a clean checkout.
	rm -rfv .make
	rm -rfv .venv

help: # List Makefile targets
	awk 'BEGIN {FS = ":.*?# "} /^[ a-zA-Z0-9_-]+:.* # / {printf "\033[36m%-41s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

.SILENT: \
	help

```

## Python

```makefile
# Ensure the virtualenvironment is created
init: .venv/bin/python3 uv.lock
# Ensure the virtual environment has the correct basic tooling before we get to the pyproject.toml
.venv/bin/python3:
	[ ! -d ".venv" ] && python3 -m venv .venv || echo ".venv already setup"
	.venv/bin/python3 -m pip install -qq --upgrade pip uv build wheel pre-commit
	.venv/bin/pre-commit install

# Ensure the lock files get generated based on changes to pyproject.toml
lock: uv.lock

uv.lock: pyproject.toml .venv/bin/python3
	.venv/bin/python3 -m uv lock --dev -U

# Install the necessary dependencies depending if it is prod or dev build
# The .make/*-deps-installed is a sentinel file we 'touch' to mark the job complete with '@touch $@'
prod: .make/prod-deps-installed
.make/prod-deps-installed: uv.lock
	.venv/bin/python3 -m uv sync
	@touch $@

dev: .make/dev-deps-installed
.make/dev-deps-installed: uv.lock
	.venv/bin/python3 -m uv sync --dev
	# If we are updating tools update aws-cdk too
	npm install -g aws-cdk
	@touch $@

# ==================== QUALITY ASSURANCE (CI) ====================

fix: .make/dev-deps-installed
	# Formatting
	.venv/bin/ruff format .
	.venv/bin/isort src/ tests/ scripts

	# Lint Fix
	.venv/bin/ruff check src/ --fix

	# Precommit validations checks
	.venv/bin/pre-commit run
	
	# Final isort to enforce import headings not yet supported in ruff
	.venv/bin/isort src/ test/ scripts

typecheck: .make/dev-deps-installed
	.venv/bin/mypy src

docs: .make/dev-deps-installed
	.venv/bin/md_toc --in-place github --header-levels 4 README.md guides/*.md
	npx cdk-dia --rendering "graphviz-png" --target infra/docs/diagrams/diagram-simple.png --collapse true --collapse-double-clusters true
	npx cdk-dia --rendering "graphviz-png" --target infra/docs/diagrams/diagram-detailed.png --collapse false --collapse-double-clusters false
	npx cdk-dia --rendering "cytoscape-html" --target infra/docs/diagrams/ --collapse false --collapse-double-clusters false    

test: .make/dev-deps-installed
	.venv/bin/python3 -m pytest

ci: fix typecheck test
```


## CDK

```makefile
```
