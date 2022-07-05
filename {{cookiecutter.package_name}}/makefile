# This ensures that we can call `make <target>` even if `<target>` exists as a file or
# directory.
.PHONY: notebook docs

# Exports all variables defined in the makefile available to scripts
.EXPORT_ALL_VARIABLES:

# Includes environment variables stored in the dotenv file
include .env
export

install-poetry:
	@echo "Installing poetry..."
	@curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -

uninstall-poetry:
	@echo "Installing poetry..."
	@curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 - --uninstall

install:
	@echo "Installing..."
	@if [ "$(shell which poetry)" == "" ]; then \
		echo "Installing poetry..."; \
		curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -; \
	fi;
	@poetry env use python3
	@poetry run python3 -m src.scripts.fix_dot_env_file
	@git init
	@git config commit.gpgsign true
	@. .env; \
		git config user.signingkey $${GPG_KEY_ID}; \
		git config user.name $${GIT_NAME}; \
		git config user.email $${GIT_EMAIL};
	@poetry install
	@poetry run pre-commit install

remove-env:
	@poetry env remove python3
	@echo "Removed virtual environment."

docs:
	@poetry run pdoc --html src/{{cookiecutter.package_name}} -o docs --force
	@echo "Saved documentation."

view-docs:
	@echo "Viewing API documentation..."
	@open docs/{{cookiecutter.package_name}}/index.html

clean:
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
	@rm -rf .pytest_cache
	@echo "Cleaned repository."
