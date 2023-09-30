# This ensures that we can call `make <target>` even if `<target>` exists as a file or
# directory.
.PHONY: docs help

# Exports all variables defined in the makefile available to scripts
.EXPORT_ALL_VARIABLES:

# Create .env file if it does not already exist
ifeq (,$(wildcard .env))
  $(shell touch .env)
endif

# Create poetry env file if it does not already exist
ifeq (,$(wildcard ${HOME}/.poetry/env))
  $(shell mkdir ${HOME}/.poetry)
  $(shell touch ${HOME}/.poetry/env)
endif

# Includes environment variables from the .env file
include .env

# Set gRPC environment variables, which prevents some errors with the `grpcio` package
export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=1
export GRPC_PYTHON_BUILD_SYSTEM_ZLIB=1

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install-poetry:
	@if [ ! "$(shell poetry --version)" = "Poetry (version 1.4.0)" ]; then \
		@pip3 install --force --quiet poetry==1.4.0; \
		@$(eval include ${HOME}/.poetry/env); \
		@echo "Installed Poetry."; \
	fi

uninstall-poetry:
	@echo "Uninstalling poetry..."
	@pip3 uninstall poetry

install: ## Install dependencies
	@echo "Installing the '{{ cookiecutter.project_name }}' project..."
	@if [ "$(shell which gpg)" = "" ]; then \
		echo "GPG not installed, so an error will occur. Install GPG on MacOS with "\
			 "`brew install gnupg` or on Ubuntu with `apt install gnupg` and run "\
			 "`make install` again."; \
	fi
	@$(MAKE) --quiet setup-python-version
	@$(MAKE) --quiet install-poetry
	@$(MAKE) --quiet setup-poetry
	@$(MAKE) --quiet setup-environment-variables
	@$(MAKE) --quiet setup-git

setup-python-version:
	@python3 src/scripts/setup_python_version.py

setup-poetry:
	@poetry env use python3 && poetry install --quiet

setup-environment-variables:
	@poetry run python src/scripts/fix_dot_env_file.py

setup-git:
	@git init
	@git config --local user.name ${GIT_NAME}
	@git config --local user.email ${GIT_EMAIL}
	@if [ ${GPG_KEY_ID} = "" ]; then \
		echo "No GPG key ID specified. Skipping GPG signing."; \
		git config --local commit.gpgsign false; \
	else \
		echo 'Just for info: If you get the "failed to sign the data" error when'\
			 'committing, try running `export GPG_TTY=$$(tty)` and `gpgconf --kill'\
			 'gpg-agent`, and try again.'; \
		git config --local commit.gpgsign true; \
		git config --local user.signingkey ${GPG_KEY_ID}; \
		echo "Signed with GPG key ID ${GPG_KEY_ID}."; \
	fi
	@poetry run pre-commit install
	@git add .
	@git commit -m "Initial commit"

docs:  ## Generate documentation
	@poetry run pdoc --docformat google src/{{cookiecutter.project_name}} -o docs
	@echo "Saved documentation."

view-docs:  ## View documentation
	@echo "Viewing API documentation..."
	@uname=$$(uname); \
		case $${uname} in \
			(*Linux*) openCmd='xdg-open'; ;; \
			(*Darwin*) openCmd='open'; ;; \
			(*CYGWIN*) openCmd='cygstart'; ;; \
			(*) echo 'Error: Unsupported platform: $${uname}'; exit 2; ;; \
		esac; \
		"$${openCmd}" docs/{{ cookiecutter.project_name }}.html

test:  ## Run tests
	@poetry run pytest && poetry run readme-cov

tree:  ## Print directory tree
	@tree -a \
		-I .git \
		-I .mypy_cache \
		-I .env \
		-I .venv \
		-I poetry.lock \
		-I .ipynb_checkpoints \
		-I dist \
		-I .gitkeep \
		-I docs \
		-I .pytest_cache \
		-I outputs \
		-I .DS_Store \
		-I .cache \
		-I raw \
		-I processed \
		-I final \
		-I checkpoint-* \
		-I .coverage* \
		-I .DS_Store \
		-I __pycache__ \
		-I .ruff_cache \
		.