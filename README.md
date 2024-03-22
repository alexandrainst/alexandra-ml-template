<a href="https://github.com/alexandrainst/{{ cookiecutter.project_name }}"><img src="https://github.com/alexandrainst/alexandra-iotml-template/blob/main/%7B%7Bcookiecutter.project_name%7D%7D/gfx/alexandra_logo.png" width="239" height="175" align="right" /></a>
# Alexandra Institute Internet of Things Repository Template

This repository is a template for an internet of things project within the Alexandra
Institute, and is the project structure we frequently use in such projects.

## Quickstart

Install Cookiecutter:
```
pip3 install cookiecutter
```

Create a project based on the template (the `-f` flag ensures that you use the newest
version of the template):
```
cookiecutter -f gh:alexandrainst/alexandra-iotml-template
```


## Features

### Automatic Documentation

Run `make docs` to create the documentation in the `docs` folder, which is based on
your docstrings in your code. You can view this by running `make view-docs`.

### Automatic Test Coverage Calculation

Run `make test` to test your code, which also updates the "coverage badge" in the
README, showing you how much of your code base that is currently being tested.

### Continuous Integration

Github CI pipelines are included in the repo, running all the tests in the `tests`
directory, as well as building online documentation if Github Pages has been enabled
for the repository (can be enabled on Github in the repository settings).

### Code Spaces

Code Spaces is a new feature on Github that allows you to develop on a project
completely in the cloud, without having to do any local setup at all. This repo comes
included with a configuration file for running code spaces on Github. When hosted on
`alexandrainst/{{ cookiecutter.project_name }}`, simply press the `<> Code` button and
add a code space to get started, which will open a VSCode window directly in your
browser.

### Flexibility in Packaging Backend

The cookiecutter allows the user to choose between `poetry` and `pip` for managing
dependencies. In both cases, `pyproject.toml` will be used for all dependencies.


## Tools used in this project
* [Grafana](https://grafana.com/): Visualisation of time series
* [PostgreSQL](https://www.postgresql.org/): Database
* [Poetry](https://towardsdatascience.com/how-to-effortlessly-publish-your-python-package-to-pypi-using-poetry-44b305362f9f): Dependency management
* [hydra](https://hydra.cc/): Manage configuration files
* [pre-commit plugins](https://pre-commit.com/): Automate code reviewing formatting
* [pdoc](https://github.com/pdoc3/pdoc): Automatically create an API documentation for your project


## Project Structure
```
.
├── .devcontainer
│   └── devcontainer.json
├── .editorconfig
├── .github
│   └── workflows
│       └── ci.yaml
├── .gitignore
├── .pre-commit-config.yaml
├── README.md
├── config
│   ├── __init__.py
│   ├── config.yaml
│   └── hydra
│       └── job_logging
│           └── custom.yaml
├── data
│   ├── final
│   │   └── .gitkeep
│   ├── processed
│   │   └── .gitkeep
│   └── raw
│       └── .gitkeep
├── docker-compose.yml
├── docs
│   └── .gitkeep
├── gfx
│   ├── .gitkeep
│   └── alexandra_logo.png
├── makefile
├── models
│   └── .gitkeep
├── notebooks
│   └── .gitkeep
├── poetry.lock
├── poetry.toml
├── pyproject.toml
├── src
│   ├── grafana
│   │   ├── dashboards
│   │   │   ├── example_dashboard.json
│   │   │   └── example_provisioning.yaml
│   │   └── datasources
│   │       └── example_datasource_provisioning.yaml
│   ├── nodered
│   │   └── example_ml_inference.json
│   ├── nodered_dockerfile
│   ├── preprocessor
│   │   ├── app.py
│   │   └── pyproject.toml
│   ├── preprocessor_dockerfile
│   ├── scripts
│   │   ├── eval_model.py
│   │   ├── fix_dot_env_file.py
│   │   ├── train_model.py
│   │   └── your_script.py
│   ├── sql
│   │   ├── database_init.sql
│   │   └── example_views.sql
│   └── test_project
│       ├── ml_tools
│       │   ├── datasets.py
│       │   ├── models.py
│       │   └── traintest.py
│       ├── utils
│       │   └── sql.py
│       └── your_module.py
└── tests
    ├── test_datasets.py
    ├── test_dummy.py
    └── test_models.py
```
