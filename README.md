<a href="https://github.com/alexandrainst/{{ cookiecutter.project_name }}">
<img
    src="https://filedn.com/lRBwPhPxgV74tO0rDoe8SpH/alexandra/alexandra-logo.jpeg"
    width="239"
    height="175"
    align="right"
/>
</a>

# Alexandra Institute Machine Learning Repository Template

This repository is a template for a Python-based data science project within the
Alexandra Institute, and is the project structure we frequently use in our data science
projects.

## Quickstart

Install Cookiecutter:
```
pip3 install cookiecutter
```

Create a project based on the template (the `-f` flag ensures that you use the newest
version of the template):
```
cookiecutter -f gh:alexandrainst/alexandra-ml-template
```


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
directory, as well as building online documentation if Github Pages has been enabled
for the repository (can be enabled on Github in the repository settings).

### Code Spaces

Code Spaces is a new feature on Github that allows you to develop on a project
completely in the cloud, without having to do any local setup at all. This repo comes
included with a configuration file for running code spaces on Github. When hosted on
`alexandrainst/<project-name>`, simply press the `<> Code` button and add a code space
to get started, which will open a VSCode window directly in your browser.
