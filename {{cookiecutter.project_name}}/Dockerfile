FROM python:{{ cookiecutter.python_version }}-slim-bookworm

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


# Move the files into the container
WORKDIR /project
COPY . /project

# Install dependencies
RUN uv sync --no-dev --no-cache

# Run the script
CMD uv run python src/scripts/main.py
