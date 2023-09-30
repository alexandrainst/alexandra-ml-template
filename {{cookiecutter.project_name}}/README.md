# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

______________________________________________________________________
[![Documentation](https://img.shields.io/badge/docs-passing-green)](https://alexandrainst.github.io/{{ cookiecutter.project_name }}/{{ cookiecutter.project_name }}.html)
[![License](https://img.shields.io/github/license/alexandrainst/{{ cookiecutter.project_name }})](https://github.com/alexandrainst/{{ cookiecutter.project_name }}/blob/main/LICENSE)
[![LastCommit](https://img.shields.io/github/last-commit/alexandrainst/{{ cookiecutter.project_name }})](https://github.com/alexandrainst/{{ cookiecutter.project_name }}/commits/main)
[![Code Coverage](https://img.shields.io/badge/Coverage-0%25-red.svg)](https://github.com/alexandrainst/{{ cookiecutter.project_name }}/tree/main/tests)


Developers:

- {{cookiecutter.author_name}} ({{cookiecutter.email}})


## Setup

### Set up the environment

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

### Automatic Documentation

Run `make docs` to create the documentation in the `docs` folder, which is based on
your docstrings in your code. You can view this by running `make view-docs`.

### Automatic Test Coverage Calculation

Run `make test` to test your code, which also updates the "coverage badge" in the
README, showing you how much of your code base that is currently being tested.



## Project structure
```
.
├── .github
│   └── workflows
│       ├── ci.yaml
│       └── docs.yaml
├── .gitignore
├── .pre-commit-config.yaml
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
├── notebooks
├── poetry.toml
├── pyproject.toml
├── src
│   ├── scripts
│   │   ├── fix_dot_env_file.py
│   │   ├── setup_python_version.py
│   │   └── versioning.py
│   └── {{ cookiecutter.project_name }}
│       └── __init__.py
└── tests
    ├── __init__.py
    └── test_dummy.py
```