"""
This script sets up the project by
installing dependencies and setting up pre-commit hooks.
"""

import subprocess
import sys
import os


def run(cmd: str):
    """
    Run a shell command and exit if it fails.

    Args
        - cmd (str): The command to run.

    """
    print(f"→ {cmd}")
    result = subprocess.run(cmd, shell=True, check=False)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main():
    """
    Defines the commands to setup the project.
    workload:
        - Upgrade pip
        - Install pip and poetry
        - Install dependencies using poetry
        - Install pre-commit hooks
    """

    if os.path.exists(".venv"):
        print("Virtual environment found. Proceeding with setup.")
        run("pip install --upgrade pip")
        run("pip install poetry")
        run("poetry update")
        run("pre-commit install")
    else:
        print("WARNING: No virtual environment '.venv'. Canceling auto-setup.")


if __name__ == "__main__":
    main()
