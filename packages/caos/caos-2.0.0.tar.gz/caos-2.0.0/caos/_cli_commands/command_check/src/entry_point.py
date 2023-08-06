import os
import re
import sys

import subprocess
from typing import List, Dict
from collections import namedtuple
from caos._internal.types import ExitCode
from caos._internal.utils.yaml import get_virtual_environment_from_yaml, Dependencies
from caos._internal.utils.working_directory import get_current_dir
from caos._internal.utils.os import is_posix_os, is_win_os
from caos._internal.utils.yaml import get_dependencies_from_yaml
from caos._internal.console import caos_command_print, INFO_MESSAGE, WARNING_MESSAGE, SUCCESS_MESSAGE, ERROR_MESSAGE
from caos._internal.constants import (
    CAOS_YAML_FILE_NAME, DEFAULT_VIRTUAL_ENVIRONMENT_NAME,
    PIP_PATH_VENV_WIN, PIP_PATH_VENV_POSIX,
    PYTHON_PATH_VENV_WIN, PYTHON_PATH_VENV_POSIX
)
from caos._cli_commands.raise_exceptions import (
    raise_missing_yaml_exception,
    raise_missing_virtual_environment_exception,
    raise_missing_pip_binary_exception,
    raise_missing_python_binary_exception
)

from .constants import NAME


def main(args: List[str]) -> ExitCode:
    current_dir: str = get_current_dir()
    if not os.path.isfile(os.path.abspath(current_dir + "/" + CAOS_YAML_FILE_NAME)):
        raise_missing_yaml_exception()

    venv_name: str = get_virtual_environment_from_yaml()

    if not os.path.isdir(os.path.abspath(current_dir + "/" + venv_name)):
        raise_missing_virtual_environment_exception(env_name=venv_name)

    if is_win_os():
        pip_path: str = PIP_PATH_VENV_WIN.replace(DEFAULT_VIRTUAL_ENVIRONMENT_NAME, venv_name)
        python_path: str = PYTHON_PATH_VENV_WIN.replace(DEFAULT_VIRTUAL_ENVIRONMENT_NAME, venv_name)
    elif is_posix_os():
        pip_path: str = PIP_PATH_VENV_POSIX.replace(DEFAULT_VIRTUAL_ENVIRONMENT_NAME, venv_name)
        python_path: str = PYTHON_PATH_VENV_POSIX.replace(DEFAULT_VIRTUAL_ENVIRONMENT_NAME, venv_name)

    if not os.path.isfile(pip_path):
        raise_missing_pip_binary_exception(env_name=venv_name)

    if not os.path.isfile(python_path):
        raise_missing_python_binary_exception(env_name=venv_name)

    if args:
        caos_command_print(
            command=NAME,
            message=WARNING_MESSAGE("The check command does not support arguments")
        )

    yaml_deps: Dependencies = get_dependencies_from_yaml()
    if not yaml_deps:
        caos_command_print(
            command=NAME,
            message=WARNING_MESSAGE("There are no dependencies defined in the '{}' file".format(CAOS_YAML_FILE_NAME))
        )
        return ExitCode(0)

    pip_list_process: subprocess.CompletedProcess = subprocess.run(
        [python_path, "-m", "pip", "list"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    if pip_list_process.returncode != 0 and pip_list_process.stderr:
        caos_command_print(
            command=NAME,
            message=ERROR_MESSAGE("It was not possible to check the virtual environment dependencies")
        )
        return ExitCode(1)

    pip_list_dependency_regex = re.compile("^(?P<name>.+)(( )+)(\()?(?P<version>((\d+)(\.\d+)?(\.\d+)?))(\))?$")
    pip_list_output_by_lines = [line.strip() for line in pip_list_process.stdout.split("\n")]

    installed_deps: Dependencies = {}
    for line in pip_list_output_by_lines:
        dep = pip_list_dependency_regex.match(line)
        if dep:
            installed_deps[dep.group("name").strip().lower()] = dep.group("version").strip()

    not_installed_deps: List[str] =[]
    for dep in yaml_deps:
        pip_dep = dep.replace("_", "-")
        if pip_dep not in installed_deps:
            not_installed_deps.append(dep)

    if not_installed_deps:
        not_installed_deps = ["'{}'".format(dep) for dep in not_installed_deps]
        caos_command_print(
            command=NAME,
            message=ERROR_MESSAGE("The following dependencies are not installed in the virtual environment: {}"
                                  .format(", ".join(not_installed_deps))
            )
        )
        return ExitCode(1)

    caos_command_print(
        command=NAME,
        message=SUCCESS_MESSAGE("All dependencies are installed in the virtual environment")
    )

    return ExitCode(0)
