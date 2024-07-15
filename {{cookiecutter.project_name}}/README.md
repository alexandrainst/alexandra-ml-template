<a href="https://github.com/alexandrainst/{{ cookiecutter.project_name }}"><img src="https://github.com/alexandrainst/{{ cookiecutter.project_name }}/raw/main/gfx/alexandra_logo.png" width="239" height="175" align="right" /></a>
# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

______________________________________________________________________
[![Code Coverage](https://img.shields.io/badge/Coverage-0%25-red.svg)](https://github.com/alexandrainst/{{cookiecutter.project_name}}/tree/main/tests){{'\n[![Documentation](https://img.shields.io/badge/docs-passing-green)](https://alexandrainst.github.io/' if cookiecutter.open_source == 'y'}}{{cookiecutter.project_name if cookiecutter.open_source == 'y'}}{{'/' if cookiecutter.open_source == 'y'}}{{ cookiecutter.project_name if cookiecutter.open_source == 'y'}}{{'.html)\n[![License](https://img.shields.io/github/license/alexandrainst/' if cookiecutter.open_source == 'y'}}{{cookiecutter.project_name if cookiecutter.open_source == 'y'}}{{')](https://github.com/alexandrainst/' if cookiecutter.open_source == 'y'}}{{cookiecutter.project_name if cookiecutter.open_source == 'y'}}{{'/blob/main/LICENSE)\n[![LastCommit](https://img.shields.io/github/last-commit/alexandrainst/' if cookiecutter.open_source == 'y'}}{{cookiecutter.project_name if cookiecutter.open_source == 'y'}}{{')](https://github.com/alexandrainst/' if cookiecutter.open_source == 'y'}}{{cookiecutter.project_name if cookiecutter.open_source == 'y'}}{{'/commits/main)\n[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.0-4baaaa.svg)](https://github.com/alexandrainst/' if cookiecutter.open_source == 'y'}}{{cookiecutter.project_name if cookiecutter.open_source == 'y'}}{{'/blob/main/CODE_OF_CONDUCT.md)' if cookiecutter.open_source == 'y'}}


Developer(s):

- {{cookiecutter.author_name}} ({{cookiecutter.email}})


## Setup

### Installation

1. Run `make install`, which sets up a virtual environment and all Python dependencies therein.
2. Run `source .venv/bin/activate` to activate the virtual environment.
3. (Optional) Run `make add-rag` to add RAG functionality from [ragger](https://github.com/alexandrainst/ragger).

### Adding and Removing Packages

To install new PyPI packages, run:
```
{{'poetry add' if cookiecutter.dependency_manager != 'pip' else 'pip install'}} <package-name>
```

To remove them again, run:
```
{{'poetry remove' if cookiecutter.dependency_manager != 'pip' else 'pip uninstall'}} <package-name>
```{{'\n\nTo freeze dependencies into pyproject.toml, run:\n```\nmake freeze\n```' if cookiecutter.dependency_manager == 'pip'}}

To show all installed packages, run:
```
{{'poetry show' if cookiecutter.dependency_manager != 'pip' else 'pip list'}}
```


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

```
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

```
from {{ cookiecutter.project_name }} import some_function
```

Note that this is also how we import functions/classes in tests, since each test Python
file is also a Python script, rather than a module.


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

### Code Spaces

Code Spaces is a new feature on Github, that allows you to develop on a project
completely in the cloud, without having to do any local setup at all. This repo comes
included with a configuration file for running code spaces on Github. When hosted on
`alexandrainst/{{ cookiecutter.project_name }}` then simply press the `<> Code` button
and add a code space to get started, which will open a VSCode window directly in your
browser.
