# Dependency Management
This project uses [_poetry_](https://python-poetry.org/) for python packaging and dependency management. The root _pyproject.toml_ file is used to maintain dependencies.
Additionally, the project uses pre-commit hooks for different tasks. These need to be activated in order to benefit from the functions.

## Dev Dependency Setup

At the project root:

__Step 1:__ Create a virtual environment  ```.venv``` in your chosen directory.

__Step 2:__ Then run:
```
python setup_dev.py
```
This will call the setup script which sets up the project automatically.

You're all set now!

---

## Useful poetry commands
- To update all dependencies, run:
```
poetry update
```
- To add a new package, run:
```
poetry add <package-name>
```
- To remove a package, run:
```
poetry remove <package-name>
```
> **Note:** It is advised to run `poetry update` after removing a package to ensure that all subdependencies are installed correctly.

- To refer to a package only used in development, add the ```--dev``` flag:
```
poetry ... --dev <package-name>
```