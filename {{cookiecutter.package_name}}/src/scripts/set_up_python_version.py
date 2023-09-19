"""Sets up compatible python version for the project, based on the current version.

Usage:
    python src/scripts/set_up_python_version.py
"""

import subprocess
from pathlib import Path
import re


def main() -> None:

    # Get Python version
    python_process = subprocess.Popen(
        ["python3", "--version"],
        stdout=subprocess.PIPE,
    )
    sed_process = subprocess.Popen(
        ["sed", "s/.* //"],
        stdin=python_process.stdout,
        stdout=subprocess.PIPE,
    )
    python_version = subprocess.check_output(
        ["sed", "s/\\(^[0-9]*\\.[0-9]*\\).*/\\1/g"],
        stdin=sed_process.stdout,
    ).decode().strip('\n')
    python_process.wait()
    sed_process.wait()

    # Set up compatible Python version in `pyproject.toml`
    compatible_python_versions = f">={python_version},<4"
    pyproject_content = Path("pyproject.toml").read_text()
    pyproject_content = re.sub(
        pattern=r"python = \".*\"",
        repl=f"python = \"{compatible_python_versions}\"",
        string=pyproject_content,
    )
    Path("pyproject.toml").write_text(pyproject_content)

    # Set up compatible Python version in `makefile`
    makefile_content = Path("makefile").read_text()
    makefile_content = re.sub(
        pattern=r"python[0-9]+(\.[0-9]+)*",
        repl=f"python{python_version}",
        string=makefile_content,
    )
    Path("makefile").write_text(makefile_content)


if __name__ == "__main__":
    main()
