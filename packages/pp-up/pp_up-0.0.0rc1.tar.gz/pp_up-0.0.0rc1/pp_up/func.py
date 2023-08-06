"""
Functions for pp_up
"""
from typing import Any, Iterable, List, Mapping, Optional, Tuple

import functools
import importlib
import re
import os

import requests
import setuptools # type: ignore

PACKAGE_MATCH = re.compile(r'[a-zA-Z_\[\]-]+')
PYPI_SESSION = requests.session()

LineResult = Tuple[str, str, str]

def get_latest_version(package: str) -> Optional[str]:
    """
    Returns the latest version for the given package

    If not found, returns None
    """
    response = PYPI_SESSION.get('https://pypi.python.org/pypi/' + package + '/json')
    if response.status_code == 404:
        return None

    assert response.ok, response.text[:1024]

    response_json = response.json()
    return str(response_json['info']['version'])

def process_line(line: str) -> Optional[LineResult]:
    """
    Processes a single pip line
    """
    if line.startswith('#') or line.startswith('-'):
        return None

    if not '==' in line:
        # Only upgrade dependencies that are pinned
        # Dependencies that are minimal don't need to be upgraded
        return None

    package, old_version = line.split('==', 1)

    if not PACKAGE_MATCH.fullmatch(package):
        return None

    new_version = get_latest_version(package)
    if new_version is None:
        return None

    old_version = old_version.strip()

    if new_version == old_version:
        return None

    return (package, old_version, new_version)

def process_requirements(filename: str, backup_suffix: str) -> None:
    """
    Processes a requirements file

    The old file will be backupped, and the versions will be updated
    """

    os.rename(filename, filename + backup_suffix)

    with open(filename + backup_suffix, 'rt') as in_file_obj, open(filename, 'wt') as out_file_obj:
        for line in in_file_obj:
            res = process_line(line)
            if res is None:
                out_file_obj.write(line)
                continue

            package, old_version, new_version = res

            print('Upgrading {} from {} to {}'.format(package, old_version, new_version))
            out_file_obj.write(line.replace(old_version, new_version))

def my_setup(
        pp_up_res_list: List[LineResult],
        install_requires: Optional[Iterable[str]] = None,
        extras_require: Optional[Mapping[str, Iterable[str]]] = None,
        **kwargs: Any,
    ) -> None:
    """
    Custom setup function so we can hook into whatever is
    send to setuptools
    """
    del kwargs

    for req in install_requires or []:
        res = process_line(req)
        if res is not None:
            pp_up_res_list.append(res)

    for _, req_list in (extras_require or {}).items():
        for req in req_list:
            res = process_line(req)
            if res is not None:
                pp_up_res_list.append(res)

def process_setup_py(filename: str, backup_suffix: str) -> None:
    """
    Processes a setup.py file

    The old file will be backupped, and the versions will be updated
    """
    res_list: List[LineResult] = []

    old_setup = setuptools.setup

    try:
        setuptools.setup = functools.partial(my_setup, res_list)

        importlib.import_module('setup')

        if not res_list:
            return

        os.rename(filename, filename + backup_suffix)

        with open(filename + backup_suffix, 'rt') as in_file_obj:
            text = in_file_obj.read()

        for res in res_list:
            package, old_version, new_version = res

            print('Upgrading {} from {} to {}'.format(package, old_version, new_version))
            text = text.replace(
                '{}=={}'.format(package, old_version),
                '{}=={}'.format(package, new_version),
            )

        with open(filename, 'wt') as out_file_obj:
            out_file_obj.write(text)

    finally:
        setuptools.setup = old_setup
