.PHONY: notebook docs
.EXPORT_ALL_VARIABLES:

install:
	@echo "Installing..."
	poetry install
	poetry run pre-commit install
	git rm -r --cached 'data/raw'
	git rm -r --cached 'data/processed'
	git rm -r --cached 'data/final'
	git rm -r --cached 'models'

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
