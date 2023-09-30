# Alexandra Institute Python Repository Template

## What is this?
This repository is a template for a Python-based data science project within the
Alexandra Institute, and is the project structure we frequently use in our data science
projects.

## How to use this project

Install Cookiecutter:
```
pip3 install cookiecutter
```

Create a project based on the template:
```
rm -rf .cookiecutters/alexandra-ml-template && cookiecutter gh:alexandrainst/alexandra-ml-template
```

## Tools used in this project
* [Poetry](https://towardsdatascience.com/how-to-effortlessly-publish-your-python-package-to-pypi-using-poetry-44b305362f9f): Dependency management
* [hydra](https://hydra.cc/): Manage configuration files
* [pre-commit plugins](https://pre-commit.com/): Automate code reviewing formatting
* [pdoc](https://github.com/pdoc3/pdoc): Automatically create an API documentation for your project

## Project Structure
```
.
├── .github
│   └── workflows
│       ├── ci.yaml
│       └── docs.yaml
├── .gitignore
├── .name_and_email
├── .pre-commit-config.yaml
├── Dockerfile
├── LICENSE
├── README.md
├── config
│   ├── __init__.py
│   ├── config.yaml
│   └── hydra
│       └── job_logging
│           └── custom.yaml
├── data
├── makefile
├── models
├── notebooks
├── poetry.toml
├── pyproject.toml
├── src
│   ├── scripts
│   │   ├── fix_dot_env_file.py
│   │   ├── setup_python_version.py
│   │   └── your_script.py
│   └── {{cookiecutter.project_name}}
│       ├── __init__.py
│       └── your_module.py
└── tests
    ├── __init__.py
    └── test_dummy.py
```
