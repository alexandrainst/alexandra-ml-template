FROM python:{{ cookiecutter.python_version }}-slim-bookworm
{{'\n# Install poetry\nRUN pip install "poetry==1.8.2"\n' if cookiecutter.dependency_manager != 'pip'}}
# Move the files into the container
WORKDIR /project
COPY . /project

# Install dependencies
{{'RUN poetry env use python' if cookiecutter.dependency_manager != 'pip'}}{{cookiecutter.python_version if cookiecutter.dependency_manager != 'pip'}}{{'\nRUN poetry install --no-interaction --no-cache --without dev' if cookiecutter.dependency_manager != 'pip' else 'RUN pip install .'}}

# Run the script
CMD {{'poetry run ' if cookiecutter.dependency_manager != 'pip'}}python src/scripts/your_script.py
