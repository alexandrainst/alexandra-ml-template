.PHONY: notebook docs
.EXPORT_ALL_VARIABLES:
export ENV_DIR = $( poetry env list --full-path | grep Activated | cut -d' ' -f1 )"

activate:
	@echo "Activating virtual environment"
	poetry shell
	source "$(ENV_DIR)/bin/activate"

install:
	@echo "Installing..."
	git init
	poetry install
	poetry run pre-commit install

delete_env:
	poetry env remove python3

pull_data:
	poetry run dvc pull

docs_view:
	@echo View API documentation...
	pdoc src --http localhost:8080

docs_save:
	@echo Save documentation to docs...
	pdoc src -o docs

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
