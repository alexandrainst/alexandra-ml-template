FROM python:{{ cookiecutter.python_version }}-slim-bookworm

# Install uv using the official image.
# From https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:{{ cookiecutter._docker_uv_version }} /uv /uvx /bin/

# Add locally installed binaries to the PATH
ENV PATH="/root/.local/bin:/project/.venv/bin/:${PATH}"

# Set /project as the working directory
WORKDIR /project

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --no-cache

# Copy the project files into the container
COPY . .

# Run the script
CMD uv run python src/scripts/main.py
