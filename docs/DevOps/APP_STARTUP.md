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

### pyproject.toml

### startup.py

### apt_installs.sh

### Threads

#### Main Thread

#### Core API Thread

#### IP API Thread

#### DM API Thread

#### UI API Thread
