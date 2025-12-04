# App Startup

## Overview

The following diagram displays the interactions between all files involved in the app startup routine.

```
<begin startup>
    |
pyproject-toml
    |
startup.py-------apt_installs.sh
    |
<end startup>
```

## Details

In the following, details for the files seen above are provided, focusing on their role in the app startup process.

### pyproject.toml

To start the application, the startup command `poetry run wave` is called.
The subcommand `run` is used to execute scripts with poetry that are defined in the `pyproject.toml` file. The script declared as `wave` points to the actual `startup.py` file, responsible for further action.

```
>pyproject.toml<

...
[tool.poetry.scripts]
wave = "scripts.startup:start"
...
```

### startup.py

This file defines the `start` method as the central entry point for the application. Here, the following tasks are handled:

1. Executing the [`apt_installs.sh`](#apt_installssh) script.
2. Starting the APIs for all modules in different threads.
3. Confirming if startup was successful up until this point. The [Main Thread](#main-thread) entering the `main` method in the Core.

### apt_installs.sh

This script is used to install Raspberry Pi-specific dependencies, which cannot be safely handled by poetry.

TODO docs when fully implemented

---

> Back to [README](../../README.md).