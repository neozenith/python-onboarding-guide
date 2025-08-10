# Containers

<!--TOC-->

- [Containers](#containers)
  - [Docker](#docker)
    - ["Basic" Dockerfile](#basic-dockerfile)
    - [Josh's "Basic" Dockerfile](#joshs-basic-dockerfile)
    - [Docker + ECR Makefile Helpers](#docker--ecr-makefile-helpers)

<!--TOC-->


## Docker

### "Basic" Dockerfile

https://www.docker.com/blog/how-to-dockerize-your-python-applications/

```Dockerfile
FROM python:3.12
# Or any preferred Python version.
ADD main.py .

RUN pip install requests beautifulsoup4 python-dotenv

CMD [“python”, “./main.py”] 
# Or enter the name of your unique directory and parameter set.
```

### Josh's "Basic" Dockerfile 

After years of rough edges and pouring over the documentation here we are:

```Dockerfile
# ==================== BUILD ====================
# Allow the Python base image version be a build argument to parametrise
ARG TARGET_PYTHON_VERSION="3.11-slim"
FROM python:${TARGET_PYTHON_VERSION} AS build

# Even in a docker container still a good idea to use a virtual environment for project dependencies
WORKDIR /usr/src/app
RUN python -m venv /usr/src/app/venv
ENV PATH="/usr/src/app/venv/bin:$PATH"

# Python tooling
RUN python3 -m pip install --no-cache-dir --upgrade pip uv

# Dependencies are compiled from pyproject.toml using `uv pip compile`. See Makefile for more details.
COPY requirements-linux.txt requirements.txt
RUN python3 -m uv pip install \
    --no-cache \
    --require-hashes \
    --no-deps \
    -r requirements.txt


# ==================== FINAL ====================
FROM python:${TARGET_PYTHON_VERSION}
ARG PROJECT_NAME
ENV PROJECT_NAME=${PROJECT_NAME}
# https://snyk.io/blog/best-practices-containerizing-python-docker/
# Do not run application as root user
# --------- ROOT USER ---------
RUN groupadd -g 999 python && \
    useradd -r -u 999 -g python python
RUN mkdir -p /usr/src/app && chown python:python /usr/src/app

# --------- NON-ROOT USER ---------
USER 999
WORKDIR /usr/src/app

# Copy virtual env from build environment across
COPY --chown=python:python --from=build /usr/src/app/venv ./venv
ENV PATH="/usr/src/app/venv/bin:$PATH"

# Source files
COPY --chown=python:python README.md README.md
COPY --chown=python:python pyproject.toml pyproject.toml
COPY --chown=python:python src/ ./src
RUN python3 -m pip install --no-cache .

# DEBUGGING: Show installed python libraries larger than 1Mb
RUN du -h -d 1 -t 1M $(python3 -c 'import sysconfig; print(sysconfig.get_path("platlib"))') | sort -rh

# NOTE: Why Your Dockerized Application Isn’t Receiving Signals
# https://hynek.me/articles/docker-signals/
# https://docs.docker.com/reference/build-checks/json-args-recommended/
ENTRYPOINT ["python3", "-m"]
CMD ["python_onboarding_guide"]

# Override CMD with:
# docker run -i -t --rm --env-file .env <image-name-kebab-case> $PROJECT_NAME --arg1 value1
# "$PROJECT_NAME --arg1 value1" was the overridden command

# Sadly interpolating variables into CMD is not available as at 2024-09-03
# https://github.com/moby/moby/issues/34772#issuecomment-2325260813
# https://docs.docker.com/build/building/variables/
```

### Docker + ECR Makefile Helpers

```Makefile
# Ensure the .make folder exists when starting make
# We need this for build targets that have multiple or no file output.
# We 'touch' files in here to mark the last time the specific job completed.
_ := $(shell mkdir -p .make)
SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

# Derive the app name from the git remote repo name and not trust what the local folder name is.
# https://stackoverflow.com/a/42543006/622276
GIT_REMOTE_URL=$(shell git config --get remote.origin.url)
APP_NAME=$(shell basename -s .git ${GIT_REMOTE_URL})
APP_NAME_KEBAB=$(APP_NAME)
APP_NAME_SNAKE=$(subst -,_,$(APP_NAME))

AWS_ACCOUNT_ID=
AWS_PROFILE=
include .env

AWS_ECR_REGION=ap-southeast-2
ECR_REGISTRY=$(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_ECR_REGION).amazonaws.com
ECR_REPOSITORY=$(ECR_REGISTRY)/$(APP_NAME_KEBAB)
DOCKER_PYTHON_BASE=3.12-slim

# Named targets are ".PHONY" and get built always. Do not depend on them in the Makefile build chain.
.PHONY: all init lock prod dev clean directory_setup docker-build docker-run docker-push docker-login debug_env

debug_env:
	@echo $(DOT_ENV_FILE)
	@echo $(AWS_PROFILE)
	@echo $(ECR_REGISTRY)

# ==================== PACKAGING / DEPLOYMENT (CD) ====================

docker-login: 
	aws --profile $(AWS_PROFILE) ecr get-login-password --region $(AWS_ECR_REGION) | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_ECR_REGION).amazonaws.com

docker-clean:
	docker buildx prune -a -f
	docker image prune -f

docker-build: 
	docker buildx build \
		--build-arg TARGET_PYTHON_VERSION=$(DOCKER_PYTHON_BASE) \
		--build-arg PROJECT_NAME=$(APP_NAME_SNAKE) \
		--progress plain \
		-t $(APP_NAME_KEBAB):latest \
		-t $(ECR_REPOSITORY):latest \
		-f containers/docker/Dockerfile \
		.
	docker tag $(APP_NAME_KEBAB):latest $(ECR_REPOSITORY):latest

docker-run:
	docker run -i -t --env-file .env $(APP_NAME_KEBAB)

docker-push: docker-build docker-login
	docker push $(ECR_REPOSITORY):latest
```
