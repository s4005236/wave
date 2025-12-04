# Dependency Management

**Why use dependency management tools?**

Aside from some academic examples, every software project relies on external resources to save development time and effort. Using libraries is a central part of creating software products.

When working in a team, it is most often needed that every developer use an agreed-upon set of dependencies. This is to ensure that bugs or problems within the code can be easily reproduced on every workstation. Managing dependencies without any designated tools is very tedious and, talking about not-so-small projects, arguably impossible.

Dependency management tools find a way to ease the handling of all external libraries needed in the development. To decide which of the many tools is the best for each project often depends on the size and type of the project at hand.

## Development Setup

> See [README](/README.md) for documentation on how to setup for development with all needed dependencies.

## Tools and Techniques

This project uses [_poetry_](https://python-poetry.org/) for Python packaging and dependency management. The root `pyproject.toml` file is used to maintain all dependencies needed for the application. 

This file is also the central place to provide information about the app. Like name, version, license, etc. It also allows for grouping the dependencies (e.g., into group `dev`) to make managing them a lot easier.

**Why use poetry for dependency management?**

> Poetry offers enough, but not much functionality and fits the project scope.

Poetry is one of many dependency management tools. In comparison to a simple `requirements.txt` with `pip` it offers useful additional functionalities (e.g., defining [scripts](./APP_STARTUP.md#pyprojecttoml)), while also being easy to use. When writing code, the developer should not have to tinker with the tool and lose focus.

## Useful poetry commands

The list below provides an overview of frequently used poetry commands. For further information, refer to the official [poetry documentation](https://python-poetry.org/docs/).

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