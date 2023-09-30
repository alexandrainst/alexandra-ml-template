"""Checks related to the .env file in the repository.

Usage:
    python src/scripts/fix_dot_env_file.py [--non-interactive]
"""

import subprocess
from pathlib import Path
import click

# List of all the environment variables that are desired
DESIRED_ENVIRONMENT_VARIABLES = dict(
    GPG_KEY_ID="Enter GPG key ID or leave empty if you do not want to use it. Type "
    "`gpg --list-secret-keys --keyid-format=long | grep sec | sed -E "
    "'s/.*\/([^ ]+).*/\\1/'` to see your key ID:\n> ",  # noqa
    GIT_NAME="Enter your full name, to be shown in Git commits:\n> ",
    GIT_EMAIL="Enter your email, as registered on your Github account:\n> ",
)


@click.command()
@click.option(
    "--non-interactive",
    is_flag=True,
    default=False,
    help="If set, the script will not ask for user input.",
)
def fix_dot_env_file(non_interactive: bool) -> None:
    """Ensures that the .env file exists and contains all desired variables.

    Args:
        non_interactive: If set, the script will not ask for user input.
    """
    env_path = Path(".env")
    name_and_email_path = Path(".name_and_email")

    # Ensure that the files exists
    env_path.touch(exist_ok=True)
    name_and_email_path.touch(exist_ok=True)

    # Extract all the lines in the files
    env_file_lines = env_path.read_text().splitlines(keepends=False)
    name_and_email_file_lines = name_and_email_path.read_text().splitlines(
        keepends=False
    )

    # Extract all the environment variables in the files
    env_vars = {line.split("=")[0]: line.split("=")[1] for line in env_file_lines}
    name_and_email_vars = {
        line.split("=")[0]: line.split("=")[1] for line in name_and_email_file_lines
    }

    # For each of the desired environment variables, check if it exists in the .env
    # file
    env_vars_missing = [
        env_var
        for env_var in DESIRED_ENVIRONMENT_VARIABLES.keys()
        if env_var not in env_vars
    ]

    # Create all the missing environment variables
    with env_path.open("a") as f:
        for env_var in env_vars_missing:
            value = ""

            if env_var in name_and_email_vars:
                value = name_and_email_vars[env_var]
            elif env_var == "GPG_KEY_ID":
                gpg = subprocess.Popen(
                    ["gpg", "--list-secret-keys", "--keyid-format=long"],
                    stdout=subprocess.PIPE,
                )
                grep = subprocess.Popen(
                    ["grep", "sec"], stdin=gpg.stdout, stdout=subprocess.PIPE
                )
                value = (
                    subprocess.check_output(
                        ["sed", "-E", "s/.*\\/([^ ]+).*/\\1/"],
                        stdin=grep.stdout,
                    )
                    .decode()
                    .strip("\n")
                )
                gpg.wait()
                grep.wait()

            if value == "" and not non_interactive:
                value = input(DESIRED_ENVIRONMENT_VARIABLES[env_var])

            f.write(f'{env_var}="{value}"\n')


if __name__ == "__main__":
    fix_dot_env_file()
