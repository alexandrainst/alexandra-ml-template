<!-- This disables the "First line in file should be a top level heading" rule -->
<!-- markdownlint-disable MD041 -->
<a href="https://github.com/alexandrainst/{{ cookiecutter.project_name }}">
<img
 width="239"
 height="175"
 align="right"
 alt="Alexandra Institute Logo"
/>
</a>

# {{ cookiecutter.project_name | replace("_", " ") | title }}

{{ cookiecutter.project_description }}

______________________________________________________________________
[![Code Coverage](https://img.shields.io/badge/Coverage-0%25-red.svg)](https://github.com/alexandrainst/{{cookiecutter.project_name}}/tree/main/tests)
{% if cookiecutter.open_source == 'y' -%}
[![Documentation](https://img.shields.io/badge/docs-passing-green)](https://alexandrainst.github.io/{{cookiecutter.project_name}})
[![License](https://img.shields.io/github/license/alexandrainst/{{cookiecutter.project_name}})](https://github.com/alexandrainst/{{cookiecutter.project_name}}/blob/main/LICENSE)
[![LastCommit](https://img.shields.io/github/last-commit/alexandrainst/{{cookiecutter.project_name}})](https://github.com/alexandrainst/{{cookiecutter.project_name}}/commits/main)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](https://github.com/alexandrainst/{{cookiecutter.project_name}}/blob/main/CODE_OF_CONDUCT.md)
{% endif %}
Developer:

- {{ cookiecutter.author_name }} (<{{ cookiecutter.email }}>)

## Setup

### Installation

1. Run `make install`, which sets up a virtual environment and all Python dependencies
   therein.
2. Run `source .venv/bin/activate` to activate the virtual environment.
3. (Optional) Run `make install-pre-commit`, which installs pre-commit hooks for
   linting, formatting and type checking.

### Adding and Removing Packages

To install new PyPI packages, run:
```bash
uv add <package-name>
```

To remove them again, run:
```bash
uv remove <package-name>
```

To show all installed packages, run:
```bash
uv pip list
```

## All Built-in Commands

The project includes the following convenience commands:

- `make install`: Install the project and its dependencies in a virtual environment.
- `make install-pre-commit`: Install pre-commit hooks for linting, formatting and type
  checking.
- `make lint`: Lint the code using `ruff`.
- `make format`: Format the code using `ruff`.
- `make type-check`: Type check the code using `mypy`.
- `make test`: Run tests using `pytest` and update the coverage badge in the readme.
- `make docker`: Build a Docker image and run the Docker container.
- `make docs`: View documentation locally in a browser.
- `make publish-docs`: Publish documentation to GitHub Pages.
- `make tree`: Show the project structure as a tree.

## A Word on Modules and Scripts
In the `src` directory there are two subdirectories, `{{ cookiecutter.project_name }}`
and `scripts`. This is a brief explanation of the differences between the two.

### Modules
All Python files in the `{{ cookiecutter.project_name }}` directory are _modules_
internal to the project package. Examples here could be a general data loading script,
a definition of a model, or a training function. Think of modules as all the building
blocks of a project.

When a module is importing functions/classes from other modules we use the _relative
import_ notation - here's an example:

```python
from .other_module import some_function
```
### Scripts
Python files in the `scripts` folder are scripts, which are short code snippets that
are _external_ to the project package, and which is meant to actually run the code. As
such, _only_ scripts will be called from the terminal. An analogy here is that the
internal `numpy` code are all modules, but the Python code you write where you import
some `numpy` functions and actually run them, that a script.

When importing module functions/classes when you're in a script, you do it like you
would normally import from any other package:

```python
from {{ cookiecutter.project_name }} import some_function
```

Note that this is also how we import functions/classes in tests, since each test Python
file is also a Python script, rather than a module.

## Features

### Docker Setup

A Dockerfile is included in the new repositories, which by default runs
`src/scripts/main.py`. You can build the Docker image and run the Docker container by
running `make docker`.

### Automatic Documentation

Run `make docs` to create the documentation in the `docs` folder, which is based on
your docstrings in your code. You can publish this documentation to Github Pages by
running `make publish-docs`. To add more manual documentation pages, simply add more
Markdown files to the `docs` directory; this will automatically be included in the
documentation.

### Automatic Test Coverage Calculation

Run `make test` to test your code, which also updates the "coverage badge" in the
README, showing you how much of your code base that is currently being tested.

### Continuous Integration

Github CI pipelines are included in the repo, running all the tests in the `tests`
directory, as well as building online documentation, if Github Pages has been enabled
for the repository (can be enabled on Github in the repository settings).

### Code Spaces

Code Spaces is a new feature on Github, that allows you to develop on a project
completely in the cloud, without having to do any local setup at all. This repo comes
included with a configuration file for running code spaces on Github. When hosted on
`alexandrainst/{{ cookiecutter.project_name }}` then simply press the `<> Code` button
and add a code space to get started, which will open a VSCode window directly in your
browser.
