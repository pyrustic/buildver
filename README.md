# Buildver
<b> Tool to build Python packages with built-in intuitive versioning mechanism </b>
    
This project is part of the [Pyrustic Open Ecosystem](https://pyrustic.github.io).
> [Installation](#installation) . [Latest](https://github.com/pyrustic/buildver/tags) . [Documentation](https://github.com/pyrustic/buildver/tree/master/docs/modules#readme)

## Table of contents
- [Overview](#overview)
- [Set a new version](#set-a-new-version)
- [Version modifiers](#version-modifiers)
- [Version width](#version-width)
- [Build a project](#build-a-project)
- [Check a project](#check-a-project)
- [API](#api)
- [Under the hood](#under-the-hood)
- [Related projects](#related-projects)
- [Installation](#installation)

# Overview
Creating distribution packages and managing version numbers are two related tasks that should be done intelligently to avoid confusion regarding version numbers. 

**Buildver** defines a standard versioning mechanism and automates the close relationship between versioning and distribution package creation while giving the developer full control.

**Buildver** is a Python package that comes as a command-line tool with an API.

This tool saves me headaches when I have to release a new version of one of my [many projects](https://pyrustic.github.io).

> **Fun fact:** **Buildver** itself is built with... **Buildver**

# Set a new version
You can change the current version of your Python project like this: `buildver set <new-version>`.

Here, `<new-version>` is either a canonical version (e.g., `3.0.1`) or a version modifier (e.g., `+rev`).

```bash
$ cd /path/to/project
$ buildver set +rev
VERSION file updated from 0.0.1 to 0.0.2

$ buildver set 0.0.3
VERSION file updated from 0.0.2 to 0.0.3
```

# Version modifiers
Use `+maj`, `+min`, and `+rev` to increment the current version of your project. 

These version modifiers increment the `major`, `minor`, and `revision` numbers respectively.

| Current | Modifier | Next   |
|---------|----------|--------|
| 1.0.0   | +rev     | 1.0.1  |
| 1.0.1   | +min     | 1.1.0  |
| 1.1.0   | +maj     | 2.0.0  |
 

# Version width
People usually limit their version scheme to 3 numbers, from left to right: the `major`, `minor`, and `revision` number. **Buildver** supports any version scheme as long as integers and dots are used. 

By default, **Buildver** works with the `major.minor.revision` scheme, but you can expand your version width, then **Buildver** will update this version according to your scheme. 

For this, **Buildver** follows simple rules:
- the `major` is the **first** number of a version
- the `minor` is the **second** number of a version
- the `revision` is the **last** number of a version

# Build a project
To build a Python distribution package with **Buildver**, simply run `buildver build`:

```bash
$ cd /path/to/demo
$ buildver build
building v0.0.1 ...
Successfully built 'demo' v0.0.1 !
VERSION file updated from 0.0.1 to 0.0.2
```

The above command will **build** a distribution package, **update** a `build_report` file then **increment** the revision number of the project version.

If you **only want to build** a distribution package, add `then pass` to the previous command:

```bash
$ cd /path/to/demo
$ buildver build then pass
building v0.0.1 ...
Successfully built 'demo' v0.0.1 !
VERSION file not updated
```

# Check a project
Get some basic information about your project with the `check` command:

```bash
$ cd /path/to/demo
$ buildver check
demo v0.0.2 (source)
.whl v0.0.1 (package) built 7 secs ago
```

# API
**Buildver** exposes an API (the same used by the CLI) with which you can interact programmatically in Python.

```python
import buildver

PROJECT_DIR = "/path/to/project"

# Set a new version
buildver.set_version("2.0.0", PROJECT_DIR)

# Get the current version
cur_version = buildver.get_version(PROJECT_DIR)  # returns "2.0.0"

# Increment the minor number with the '+min' version modifier
new_version = buildver.interpret_version(cur_version, "+min")  # returns "2.1.0"
buildver.set_version(new_version, PROJECT_DIR)

# Build the project
success, errors = buildver.build_project(PROJECT_DIR)

if success:
    # Update the build_report file
    buildver.update_build_report(new_version, PROJECT_DIR)

# Get the latest build info
version, timestamp = buildver.get_latest_build(PROJECT_DIR)

```

> **Read the [modules documentation](https://github.com/pyrustic/buildver/tree/master/docs/modules#readme).**

# Under the hood
To build a `.whl` Python distribution package, **Buildver** uses [Subrun](https://github.com/pyrustic/subrun) to run the `setup.py` module on the root of a Python project.

The project version is stored in a `VERSION` file at the root. This file is referenced in `setup.cfg`. So you can safely read and write the `VERSION` file. Obviously, it is recommended to use **Buildver** to change the version of the project.

The `build_report` file is located in `$PROJECT_DIR/.pyrustic/buildver`. 

Each line of this file can be split into two parts: the `version` on the left and the `timestamp` on the right. The first line represents the latest build.

# Related projects
Following are some related projects.

## Setupinit
**Buildver** needs your project to follow a standard Python project structure in order to build it.
**Setupinit** is a command line tool to properly initialize your Python project.

> **Discover [Setupinit](https://github.com/pyrustic/setupinit#readme) !**


## Backstage
**Backstage** is a **language-agnostic** command-line tool that allows the developer to define, coordinate and use the various resources at his disposal to create and manage a software project.

**Backstage**'s default behavior involves using **Buildver**.

> **Discover [Backstage](https://github.com/pyrustic/backstage#readme) !**

# Installation
**Buildver** is **cross platform** and versions under **1.0.0** will be considered **Beta** at best. It is built on [Ubuntu](https://ubuntu.com/download/desktop) with [Python 3.8](https://www.python.org/downloads/) and should work on **Python 3.5** or **newer**.

## For the first time

```bash
$ pip install buildver
```

## Upgrade
```bash
$ pip install buildver --upgrade --upgrade-strategy eager

```

<br>
<br>
<br>

[Back to top](#readme)