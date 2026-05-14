"""Post-generation cleanup.

Cookiecutter writes a directory whose name renders to an empty string into the
parent directory, which silently corrupts the output (children land in the
wrong place, or worse, at the filesystem root). To keep generation robust, the
frontend directories are always written and removed here when not wanted.
"""

from __future__ import annotations

import shutil
from pathlib import Path

INCLUDE_FRONTEND = "{{ cookiecutter.include_frontend }}" == "y"

FRONTEND_PATHS = [Path("public"), Path("src") / "frontend"]


def main() -> None:
    if not INCLUDE_FRONTEND:
        for path in FRONTEND_PATHS:
            if path.exists():
                shutil.rmtree(path)


if __name__ == "__main__":
    main()
