# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

Developers:

- {{cookiecutter.author_name}} ({{cookiecutter.email}})


## Setup

### Set up the environment
1. If you do not have [Poetry](https://python-poetry.org/docs/#installation) then
   install it:
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
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

### Run the entire pipeline
To run the entire pipeline, type:
```bash
dvc repo
```

### Version your data
Read [this article](https://towardsdatascience.com/introduction-to-dvc-data-version-control-tool-for-machine-learning-projects-7cb49c229fe0) on how to use DVC to version your data.

Basically, you start with setting up a remote storage. The remote storage is where your data is stored. You can store your data on DagsHub, Google Drive, Amazon S3, Azure Blob Storage, Google Cloud Storage, Aliyun OSS, SSH, HDFS, and HTTP.

```bash
dvc remote add -d remote <REMOTE-URL>
```

Commit the config file:
```bash
git commit .dvc/config -m "Configure remote storage"
```

Push the data to remote storage:
```bash
dvc push
```

Add and push all changes to Git:
```bash
git add .
git commit -m 'commit-message'
git push origin <branch>
```

### Auto-generate API documentation

To auto-generate API document for your project, run:

```bash
make docs
```

## Tools used in this project
* [Poetry](https://towardsdatascience.com/how-to-effortlessly-publish-your-python-package-to-pypi-using-poetry-44b305362f9f): Dependency management
* [hydra](https://hydra.cc/): Manage configuration files
* [pre-commit plugins](https://pre-commit.com/): Automate code reviewing formatting
* [DVC](https://dvc.org/): Data version control
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
│   ├── final                       # data after training the model
│   ├── processed                   # data after processing
│   ├── raw                         # raw data
│   └── raw.dvc                     # DVC file of data/raw
├── docs                            # documentation for your project
├── dvc.yaml                        # DVC pipeline
├── .flake8                         # configuration for flake8 - a Python formatter tool
├── .gitignore                      # ignore files that cannot commit to Git
├── makefile                        # store useful commands to set up the environment
├── models                          # store models
├── notebooks                       # store notebooks
├── .pre-commit-config.yaml         # configurations for pre-commit
├── pyproject.toml                  # dependencies for poetry
├── README.md                       # describe your project
├── src                             # store source code
│   ├── __init__.py                 # make src a Python module
│   └── demo.py                     # demo module
└── tests                           # store tests
    └── __init__.py                 # make tests a Python module
```
