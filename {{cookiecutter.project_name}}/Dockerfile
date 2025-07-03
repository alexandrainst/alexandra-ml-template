FROM python:{{ cookiecutter.python_version }}-slim-bookworm

# Install uv (note: the script itself also requires curl)
RUN apt-get update && apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:/project/.venv/bin/:${PATH}"

WORKDIR /project

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --no-cache

# Copy the project files into the container
COPY . .

# Run the script
CMD uv run python src/scripts/main.py
