# Dependency Management

## Development Setup

> See [README](/README.md) for documentation on how to setup for development with all needed dependencies.

## Tools and Techniques

This project uses [_poetry_](https://python-poetry.org/) for python packaging and dependency management. The root `pyproject.toml` file is used to maintain all dependencies needed for the application. 

This file is also the central place to provide information about the app. Like name, version, licence etc. It also allows for grouping the dependencies (e.g. into group `dev`) to make managing them a lot easier.

## Useful poetry commands

The list below provides an overview over frequently used poetry commands. For further information refer to the official [poetry documentation](https://python-poetry.org/docs/).

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

---

> Back to [DevOps](./_DEV_OPS.md).