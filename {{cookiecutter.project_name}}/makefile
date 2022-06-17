.PHONY: notebook docs
.EXPORT_ALL_VARIABLES:

activate:
	@echo "Activating virtual environment..."
	@poetry shell
	@source `poetry env info --path`/bin/activate

install:
	@echo "Installing..."
	@git init
	@if [ "{{cookiecutter.gpg_key_id}}" != "Type `gpg --list-keys` to see your key IDs" ]; then\
		git config commit.gpgsign true;\
		git config user.signingkey "{{cookiecutter.gpg_key_id}}";\
	fi
	@git config user.email "{{cookiecutter.email}}"
	@git config user.name "{{cookiecutter.author_name}}"
	@poetry install
	@poetry run pre-commit install

remove-env:
	@poetry env remove python3
	@echo "Removed virtual environment."

view-docs:
	@echo "Viewing API documentation..."
	@pdoc src/{{cookiecutter.project_name}}

docs:
	@pdoc src/{{cookiecutter.project_name}} -o docs
	@echo "Saved documentation."

clean:
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
	@rm -rf .pytest_cache
	@echo "Cleaned repository."
