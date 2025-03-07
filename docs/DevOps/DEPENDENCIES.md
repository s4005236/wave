# Dependencies
Dependencies refer to all the external libraries, packages, or modules that the project needs to work properly.

## Goal
The goal is to give each module its specific dependencies, while still making it easy to install the requirements of the entire system without too much hassle.

## Structure
This project uses _poetry_ for python packaging and dependency management. The pyproject.toml files are used to maintain global dependencies as well as local ones in the specific submodules. When setting up globally, all the local dependencies get merged by the pyproject.toml at root, so there is no need to setup all the modules manually.

## Dev Dependency Setup
> The steps below apply to both global and local submodule setups.

At the project root or in one of the submodules ```src/<module-name>```:

Preferably create a virtual environment  ```.venv``` in your chosen directory.

Then run:
```
pip install poetry
poetry update
```
This will install all packages currently specified in the pyproject.toml via _poetry_.

---

- To add a new package, run:
```
poetry add <package-name>
```
- To remove a package, run:
```
poetry remove <package-name>
```
- To refer to a package only used in development, add the ```--dev``` flag:
```
poetry ... --dev <package-name>
```
