"""
This script is used in the package github action to setup the project.
"""

import subprocess
import sys


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
    """
    run("python -m pip install --upgrade pip")
    run("pip install poetry")
    run("poetry update")
    run("pip install poetry")


if __name__ == "__main__":
    main()
