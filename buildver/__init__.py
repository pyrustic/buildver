import os
import os.path
import time
import subrun
from buildver import error


def get_version(project_dir=None):
    """
    This function read the VERSION file in the project_dir project
    then returns the version (str) of the project.

    [parameters]
    - project_dir: str, path to the project_dir project (default to os.getcwd)

    [exceptions]
    - error.MissingVersionFileError: raised when the VERSION file is missing

    [return]
    str, version extracted from $PROJECT_DIR/VERSION or None
    """
    if not project_dir:
        project_dir = os.getcwd()
    path = os.path.join(project_dir, "VERSION")
    if not os.path.exists(path):
        raise error.MissingVersionFileError
    with open(path, "r") as file:
        lines = file.readlines()
    if not lines:
        return None
    line = lines[0]
    cache = []
    for char in line:
        if char not in (" ", "\n"):
            cache.append(char)
    version = "".join(cache)
    version = None if (not version or version.isspace()) else version
    return version


def set_version(version, project_dir=None):
    """
    This function edits the content of $PROJECT_DIR/VERSION

    [parameters]
    - version: str, the version
    - project_dir: str, path to the project_dir project (default: os.getcwd)

    [exceptions]
    - item: val

    [return]
    Returns False if the project_dir doesn't exist, returns True if all right
    """
    if not project_dir:
        project_dir = os.getcwd()
    if not os.path.exists(project_dir):
        return False
    path = os.path.join(project_dir, "VERSION")
    with open(path, "w") as file:
        file.write(version)
    return True


def interpret_version(cur_version, new_version):
    """
    This function interprets the command to set a new version.

    [parameters]
    - cur_version: str, the current version, the one to alter.
    - new_version: str, the new version. It can be a canonical version like "0.0.1"
    or a version modifier like "+rev" or "pass".
    Use "+maj" to increment the major number of the current version,
    "+min" to increment the minor number of the current version,
    and "+rev": to increment the revision number of the current version.

    [return]
    The new version as it should be saved in $PROJECT_DIR/VERSION
    """
    if new_version == "pass":
        return cur_version
    if new_version not in ("+maj", "+min", "+rev"):
        return new_version
    cache = cur_version.split(".")
    cache_size = len(cache)
    if cache_size == 1:
        cache.extend(["0", "0"])
    # interpret '+maj', '+min' and '+rev'
    if new_version == "+maj":
        cache[0] = _increment(cache[0])
        _reset_to_zero(cache, 1, cache_size)
    elif new_version == "+min":
        cache[1] = _increment(cache[1])
        _reset_to_zero(cache, 2, cache_size)
    elif new_version == "+rev":
        cache[-1] = _increment(cache[-1])
    version = ".".join(cache)
    return version


def build_project(project_dir=None):
    """
    Build the project

    [parameters]
    - project_dir: str, project dir (default: os.getcwd)

    [return]
    Returns a tuple: success_boolean, error_str
        """
    if not project_dir:
        project_dir = os.getcwd()
    command = "python -m setup --quiet sdist bdist_wheel"
    info = subrun.ghostrun(command, cwd=project_dir)
    success = True
    if info.return_code != 0:
        success = False
    return success, info.error


def get_latest_build(project_dir=None):
    """
    Get basic information about the latest build

    [parameters]
    - project_dir: str, project dir (default: os.getcwd)

    [return]
    Returns a tuple of strings: (version, timestamp).
    Return None if there is nothing to show.
    """
    if not project_dir:
        project_dir = os.getcwd()
    build_report_path = os.path.join(project_dir, ".pyrustic",
                                     "buildver", "build_report")
    if not os.path.isfile(build_report_path):
        return None
    with open(build_report_path, "r") as file:
        line = file.readline()
        if not line:
            return None
    version, timestamp = line.split()
    return version, timestamp


def update_build_report(version, project_dir=None):
    """
    Update the build_report file

    [parameters]
    - version: str, version at its canonical form
    - project_dir: str, project dir (default: os.getcwd)

    [return]
    None
    """
    if not project_dir:
        project_dir = os.getcwd()
    build_report_dir = os.path.join(project_dir, ".pyrustic",
                                    "buildver")
    if not os.path.isdir(build_report_dir):
        os.makedirs(build_report_dir)
    build_report_path = os.path.join(build_report_dir, "build_report")
    if not os.path.isfile(build_report_path):
        with open(build_report_path, "w") as file:
            pass
    text = "{} {}".format(version, int(time.time()))
    # readlines
    with open(build_report_path, "r") as file:
        lines = file.readlines()
        lines.insert(0, "{}\n".format(text))
    # update build report file
    with open(build_report_path, "w") as file:
        data = "".join(lines[0:999])
        file.write(data)


def _increment(number):
    number = int(number) + 1
    return str(number)


def _reset_to_zero(target, from_index, to_index):
    for i in range(from_index, to_index):
        target[i] = "0"
