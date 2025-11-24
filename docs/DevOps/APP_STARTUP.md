# App Startup

## Overview

The following diagram displays the interactions between all files involves in the app startup routine.

```
Terminal
|
pyproject-toml
|
startup.py-------apt_installs.sh
|
-----------------------------------------------------------------
|                   |               |               |           |
main            core api        ip api          dm api          ui api
|


```

## Tasks

The specific parts of the routine distributed over the files seen above shall now be explained in further detail.

### Terminal / pyproject.toml

To start the application, the `poetry run wave` command is called.
The subcommand `run` is used to execute scripts with poetry which are defined in the `pyproject.toml` file. The script declared as `wave` points to the actual `startup.py` file, responsible for further action.

```
>pyproject.toml<

...
[tool.poetry.scripts]
wave = "scripts.startup:start"
...
```

### startup.py

This file defines the `start` method as the central entry point for the application. Here, the following tasks are handled:

1. Calling the [`apt_installs.sh`](#apt_installssh) script.
2. Starting the [Core REST API](#core-api-thread) in a separate thread.
3. Starting the [Image Processor REST API](#image-processor-api-thread) in a separate thread.
4. TODO doc the other threads
5. The [Main Thread](#main-thread) entering the `main` method in the Core.

### apt_installs.sh

TODO docs when implemented

### Threads

#### Main Thread

sends gestures, goes into while loop forever

#### Core API Thread

#### Image Processor API Thread

#### Device Manager API Thread

TODO docs

#### UI API Thread

TODO docs

---

> Back to [README](../../README.md).