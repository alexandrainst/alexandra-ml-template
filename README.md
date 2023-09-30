<a href="https://github.com/alexandrainst/{{ cookiecutter.project_name }}"><img src="https://github.com/alexandrainst/alexandra-ml-template/blob/main/%7B%7Bcookiecutter.project_name%7D%7D/gfx/alexandra_logo.png" width="239" height="175" align="right" /></a>
# Alexandra Institute Python Repository Template

## What is this?
This repository is a template for a Python-based data science project within the
Alexandra Institute, and is the project structure we frequently use in our data science
projects.

## Quickstart

### Creating a New Project

Install Cookiecutter:
```
pip3 install cookiecutter
```

Create a project based on the template:
```
rm -rf .cookiecutters/alexandra-ml-template && cookiecutter gh:alexandrainst/alexandra-ml-template
```

### Setting up a New Project

After you've built the repository, you can now install the project as follows:

1. Run `make install`, which installs Poetry (if it isn't already installed), sets up a virtual environment and all Python dependencies therein.
2. Run `source .venv/bin/activate` to activate the virtual environment.

### Package Management

To install new PyPI packages, run:

```
poetry add <package-name>
```

To remove them again, run:
```
poetry remove <package-name>
```

To show all installed packages, run:
```
poetry show
```

## Features

### Docker Setup

A Dockerfile is included in the new repositories, which by default runs
`src/scripts/your_script.py`. You can build the Docker image and run the Docker
container by running `make docker`.

### Automatic Documentation

Run `make docs` to create the documentation in the `docs` folder, which is based on
your docstrings in your code. You can view this by running `make view-docs`.

### Automatic Test Coverage Calculation

Run `make test` to test your code, which also updates the "coverage badge" in the
README, showing you how much of your code base that is currently being tested.

### Continuous Integration

Github CI pipelines are included in the repo, running all the tests in the `tests`
directory, as well as building online documentation, if Github Pages has been enabled
for the repository (can be enabled on Github in the repository settings).


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
├── gfx
│   └── alexandra_logo.png
├── makefile
├── models
├── notebooks
├── poetry.toml
├── pyproject.toml
├── src
│   ├── scripts
│   │   ├── fix_dot_env_file.py
│   │   └── your_script.py
│   └── {{cookiecutter.project_name}}
│       ├── __init__.py
│       └── your_module.py
└── tests
    ├── __init__.py
    └── test_dummy.py
```
