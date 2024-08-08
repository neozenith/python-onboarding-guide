
all: init lock dev fix docs

init: .venv/bin/python3

.venv/bin/python3:
	[ ! -d ".venv" ] && python3 -m venv .venv || echo ".venv already setup"
	.venv/bin/python3 -m pip install -qq --upgrade pip uv wheel pre-commit
	.venv/bin/pre-commit install

lock: requirements%.txt

requirements%.txt: pyproject.toml
	.venv/bin/python3 -m uv pip compile --generate-hashes --upgrade  -o requirements.txt pyproject.toml
	.venv/bin/python3 -m uv pip compile --extra dev --upgrade  -o requirements-dev.txt pyproject.toml


prod: requirements.txt
	.venv/bin/python3 -m uv pip install \
    	--require-hashes --no-deps \
    	-r requirements.txt
	.venv/bin/python3 -m uv pip install .  # <- the app/pkg itself


dev: requirements-dev.txt
	.venv/bin/python3 -m uv pip install \
    	-r requirements-dev.txt \
    	--editable .  # <- the app/pkg itself

fix: dev
	.venv/bin/ruff format .
	.venv/bin/ruff check . --fix
	.venv/bin/pre-commit run
	.venv/bin/isort .

docs:
	.venv/bin/md_toc --in-place github --header-levels 4 README.md guides/*.md

test: dev
	.venv/bin/python3 -m pytest

clean:
	rm -rfv .venv
	rm -rfv dbt_projects
	rm -rfv requirements.txt requirements-dev.txt

quickstart: clean init lock dev

deploy: clean init lock prod

.PHONY: clean init update dev prod quickstart deploy docs
