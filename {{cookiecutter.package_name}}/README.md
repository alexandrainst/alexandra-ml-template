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
├── LICENSE
├── README.md
├── config
│   ├── main.yaml
│   ├── model
│   │   └── model1.yaml
│   └── process
│       └── process1.yaml
├── data
│   ├── final
│   ├── processed
│   └── raw
├── docs
├── makefile
├── models
├── notebooks
├── pyproject.toml
├── src
│   └── {{cookiecutter.package_name}}
│       ├── __init__.py
│       └── demo.py
└── tests
    └── __init__.py
```
