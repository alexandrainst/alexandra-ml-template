FROM python:{{ cookiecutter.python_version }}-slim-bookworm

# Install uv
COPY --from=ghcr.io/astral-sh/uv:{{ cookiecutter._docker_uv_version }} /uv /uvx /bin/


# Move the files into the container
WORKDIR /project
COPY . /project

# Install dependencies
RUN uv sync --no-dev --no-cache

# Run the script
CMD uv run python src/scripts/main.py
