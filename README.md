# Data Science Cookie Cutter

## What is this?
This repository is a template for a data science project. This is the project structure
I frequently use for my data science projects.

## How to use this project

Install Cookiecutter:
```
$ python3 -m pip install --user cookiecutter
```

Create a project based on the template:
```
$ cookiecutter gh:saattrupdan/saattrupdan-template
```

## Tools used in this project
* [Poetry](https://towardsdatascience.com/how-to-effortlessly-publish-your-python-package-to-pypi-using-poetry-44b305362f9f): Dependency management
* [hydra](https://hydra.cc/): Manage configuration files
* [pre-commit plugins](https://pre-commit.com/): Automate code reviewing formatting
* [pdoc](https://github.com/pdoc3/pdoc): Automatically create an API documentation for your project

## Project Structure
```
.
├── .flake8
├── .github
│   └── workflows
│       ├── ci.yaml
│       └── docs.yaml
├── .gitignore
├── .pre-commit-config.yaml
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── config
│   ├── __init__.py
│   └── config.yaml
├── data
├── makefile
├── models
├── notebooks
├── poetry.toml
├── pyproject.toml
├── src
│   ├── scripts
│   │   ├── fix_dot_env_file.py
│   │   └── versioning.py
│   └── {{cookiecutter.package_name}}
│       └── __init__.py
└── tests
    ├── __init__.py
    └── test_dummy.py
```
