# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

Developers:

- {{cookiecutter.author_name}} ({{cookiecutter.email}})


## Setup

### Set up the environment
1. If you do not have [Poetry](https://python-poetry.org/docs/#installation) then
   install it:
```bash
make install-poetry
```
2. Set up the environment:
```bash
make activate
make install
```

### Install new packages
To install new PyPI packages, run:
```bash
poetry add <package-name>
```

### Auto-generate API documentation

To auto-generate API document for your project, run:

```bash
make docs
```

To view the documentation, run:

```bash
make view-docs
```

## Tools used in this project
* [Poetry](https://towardsdatascience.com/how-to-effortlessly-publish-your-python-package-to-pypi-using-poetry-44b305362f9f): Dependency management
* [hydra](https://hydra.cc/): Manage configuration files
* [pre-commit plugins](https://pre-commit.com/): Automate code reviewing formatting
* [pdoc](https://github.com/pdoc3/pdoc): Automatically create an API documentation for your project

## Project structure
```bash
.
├── config
│   ├── main.yaml                   # Main configuration file
│   ├── model                       # Configurations for training model
│   │   └── model1.yaml             # First variation of parameters to train model
│   └── process                     # Configurations for processing data
│       └── process1.yaml           # First variation of parameters to process data
├── data
│   ├── final                       # Data after training the model
│   ├── processed                   # Data after processing
│   └── raw                         # Raw data
├── docs                            # Documentation for the project
├── .flake8                         # Configuration for the linting tool flake8
├── .gitignore
├── makefile
├── models                          # Trained machine learning models
├── notebooks                       # Jupyter notebooks
├── .pre-commit-config.yaml         # Configurations for pre-commit hook
├── pyproject.toml                  # Project setup
├── README.md                       # Description of the project
├── src                             # All source code
│   └── {{cookiecutter.project_name}}
│      ├── __init__.py
│      └── demo.py                  # Demo module
└── tests                           # Unit tests
    └── __init__.py
```
