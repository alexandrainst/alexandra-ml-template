FROM python:{{ cookiecutter.python_version }}-slim-bookworm

{%- if cookiecutter.dependency_manager != 'pip' %}

# Install Poetry
RUN pip install "poetry=={{ cookiecutter._poetry_version }}"
{%- endif %}

# Move the files into the container
WORKDIR /project
COPY . /project

# Install dependencies
{% if cookiecutter.dependency_manager != 'pip' -%}
RUN poetry env use python {{ cookiecutter.python_version }}
RUN poetry install --no-interaction --no-cache --without dev
{%- else -%}
RUN python3 -m venv .venv
RUN . .venv/bin/activate && pip install .
{%- endif %}

# Run the script
{% if cookiecutter.dependency_manager != 'pip' -%}
CMD poetry run python src/scripts/main.py
{%- else -%}
CMD . .venv/bin/activate && python src/scripts/main.py
{%- endif %}
