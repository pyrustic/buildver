"""Command line interface"""
import os
import os.path
import time
import buildver
from buildver import error


__all__ = []


HELP = """\
Build and versioning tool for Python projects.

Check a project
===============
$ buildver check

Set a new version 
=================
$ buildver set <version>

Build your project 
==================
$ buildver build

Build then set a new version
============================
$ buildver build then <version>


Note: Use "+maj", "+min" and "+rev" to increment
the current version of your project. These version
modifiers increment the "major", "minor", and "revision"
numbers respectively.

 Current | Modifier | Next   |
---------|----------|--------|
 1.0.0   | +rev     | 1.0.1  |
 1.0.1   | +min     | 1.1.0  |
 1.1.0   | +maj     | 2.0.0  |
 
By default, the command "build" will build a distribution
package, then automatically increment the revision number
of the current version. If you don't want the version number
incremented automatically, use the "pass" modifier:
$ buildver build then pass

Read more online:
https://github.com/pyrustic/buildver
"""


def print_help(*args, project_dir=None):
    print(HELP)


def check_project(*args, project_dir=None):
    project_dir = project_dir if project_dir else os.getcwd()
    try:
        project_version = buildver.get_version(project_dir)
    except error.MissingVersionFileError as e:
        print("Missing VERSION file.")
        return
    else:
        if not project_version:
            project_version = "0.0.0"
            buildver.set_version(project_version, project_dir)
    project_name = os.path.basename(project_dir)
    print("{} v{} (source)".format(project_name, project_version))
    # Latest build
    latest_build_info = buildver.get_latest_build(project_dir)
    if not latest_build_info:
        return
    version, timestamp = latest_build_info
    time_elapsed = _stringify_time_elapsed(timestamp)
    time_elapsed = "{}".format(time_elapsed) if time_elapsed else ""
    print(".whl v{} (package) built {}".format(version, time_elapsed))


def set_version(*args, project_dir=None):
    if not args:
        print("Missing version number.")
        return
    if len(args) > 1:
        print("Wrong usage of the command.")
        return
    project_dir = project_dir if project_dir else os.getcwd()
    new_version = args[0]
    if " " in new_version:
        print("Invalid version.")
        return
    current_version = None
    try:
        current_version = buildver.get_version(project_dir)
    except error.MissingVersionFileError as e:
        pass
    current_version = current_version if current_version else "0.0.0"
    if new_version:
        try:
            new_version = buildver.interpret_version(current_version, new_version)
        except ValueError as e:
            print("Failed to set the version. Please check the VERSION file.")
            return
        except Exception as e:
            print("Failed to set the version.")
            return
    else:
        new_version = "0.0.1"
    if current_version == new_version:
        print("VERSION file not updated")
    else:
        buildver.set_version(new_version, project_dir)
        print("VERSION file updated from {} to {}".format(current_version,
                                                          new_version))


def build_project(*args, project_dir=None):
    if not args:
        next_version = "+rev"
    elif len(args) == 1:
        print("Wrong usage of the command.")
        return
    else:
        if args[0] == "then":
            next_version = args[1]
        else:
            print("Wrong usage of the command.")
            return
    project_dir = project_dir if project_dir else os.getcwd()
    try:
        cur_version = buildver.get_version(project_dir)
    except error.MissingVersionFileError as e:
        print("Missing VERSION file.")
        return
    # BUILD
    print("building v{} ...".format(cur_version))
    success, _ = buildver.build_project(project_dir)
    if success:
        buildver.update_build_report(cur_version, project_dir)
    else:
        print("Failed to build a distribution package")
        return
    project_name = os.path.basename(project_dir)
    print("Successfully built '{}' v{} !".format(project_name, cur_version))
    # set next version
    set_version(next_version, project_dir=project_dir)


def _stringify_time_elapsed(timestamp):
    if not timestamp:
        return ""
    timestamp = int(timestamp)
    now = time.time()
    seconds_elapsed = int(now - timestamp)
    years, days, hours, minutes, seconds = _time_elapsed(seconds_elapsed)
    if years:
        return _x_ago(years, "year")
    if days:
        return _x_ago(days, "day")
    if hours:
        return _x_ago(hours, "hour")
    if minutes:
        return _x_ago(minutes, "min")
    if seconds:
        return _x_ago(seconds, "sec")


def _x_ago(x, name):
    plural = ""
    if x > 1:
        plural = "s"
    return "{} {}{} ago".format(x, name, plural)


def _time_elapsed(seconds_elapsed):
    s_in_min = 60
    s_in_hour = s_in_min * 60
    s_in_day = s_in_hour * 24
    s_in_year = s_in_day * 365
    years, remainder = divmod(seconds_elapsed, s_in_year)
    days, remainder = divmod(seconds_elapsed, s_in_day)
    hours, remainder = divmod(remainder, s_in_hour)
    minutes, seconds = divmod(remainder, s_in_min)
    return years, days, hours, minutes, seconds
