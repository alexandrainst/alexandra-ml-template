# Data Science Cookie Cutter

## What is this?
This repository is a template for a data science project. This is the project structure
I frequently use for my data science projects.

## Tools used in this project
* [Poetry](https://towardsdatascience.com/how-to-effortlessly-publish-your-python-package-to-pypi-using-poetry-44b305362f9f): Dependency management
* [hydra](https://hydra.cc/): Manage configuration files
* [pre-commit plugins](https://pre-commit.com/): Automate code reviewing formatting
* [pdoc](https://github.com/pdoc3/pdoc): Automatically create an API documentation for your project

## Project Structure
```bash
.
├── .env
├── .flake8
├── .github
│   └── workflows
│       └── ci.yml
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE
├── README.md
├── config
│   ├── __init__.py
│   ├── config.yaml
│   ├── model
│   │   └── model1.yaml
│   └── process
│       └── process1.yaml
├── data
│   ├── final
│   │   └── .gitkeep
│   ├── processed
│   │   └── .gitkeep
│   └── raw
│       └── .gitkeep
├── docs
│   └── .gitkeep
├── makefile
├── models
│   └── .gitkeep
├── notebooks
│   └── .gitkeep
├── poetry.toml
├── pyproject.toml
├── src
│   ├── scripts
│   │   └── fix_dot_env_file.py
│   └── {{cookiecutter.package_name}}
│       ├── __init__.py
│       └── demo.py
└── tests
    └── __init__.py
```

## How to use this project

Install Cookiecutter:
```bash
python3 -m pip install --user cookiecutter
```

Create a project based on the template:
```bash
cookiecutter https://github.com/saattrupdan/saattrupdan-template
```
