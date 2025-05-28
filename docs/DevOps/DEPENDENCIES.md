# Dependencies
Dependencies refer to all the external libraries, packages, or modules that the project needs to work properly.

## Goal
The goal is to give each module its specific dependencies, while still making it easy to install the requirements of the entire system without too much hassle.

## Structure
This project uses [_poetry_](https://python-poetry.org/) for python packaging and dependency management. The _pyproject.toml_ files are used to maintain global dependencies as well as local ones in the specific submodules. When setting up globally, all the local dependencies get merged by the _pyproject.toml_ at root, so there is no need to setup all the modules manually.
Additionally, the project uses pre-commit hooks for different tasks. These need to be activated in order to benefit from the functions.

## Dev Dependency Setup
> The steps below apply to both global and local submodule setups.

At the project root or in one of the submodules ```src/<module-name>```:

__Step 1:__ Create a virtual environment  ```.venv``` in your chosen directory.

__Step 2:__ Then you can run:
```
python setup_dev.py
```
This will call the setup script which does the following commands for you and sets up the project automatically.

You're all set now!

---

__Alternatively:__ When setting up manually, instead of Step 2 you should run:
```
pip install poetry
poetry update
pre-commit install
```
This will install all packages currently specified in the pyproject.toml via _poetry_
and also install all pre-commit hooks.

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