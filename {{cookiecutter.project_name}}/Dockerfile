FROM python:{{ cookiecutter.python_version }}-slim-bookworm
{{'\n# Install poetry\nRUN pip install "poetry==1.5.1"\n\n' if cookiecutter.dependency_manager != 'pip' else ''}}
# Move the files into the container
WORKDIR /project
COPY . /project

# Install dependencies
{{'RUN poetry env use python{{ cookiecutter.python_version }}\nRUN poetry install --no-interaction --no-cache --without dev' if cookiecutter.dependency_manager != 'pip' else 'RUN pip install .'}}

# Run the script
CMD {{'poetry run ' if cookiecutter.dependency_manager != 'pip' else ''}}python{{cookiecutter.python_version}} src/scripts/your_script.py
