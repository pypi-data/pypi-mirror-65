"""
Main module to call `python -m pp_up` from command line
"""
import os
import sys

from .func import process_requirements, process_setup_py

BACKUP_SUFFIX = '~'
REQUIREMENTS_FILE_NAMES = ['requirements.txt', 'requirements-dev.txt']

def main() -> int:
    """
    Main method
    """
    for file_name in REQUIREMENTS_FILE_NAMES:
        if not os.path.isfile(file_name):
            continue

        process_requirements(file_name, BACKUP_SUFFIX)

    if os.path.isfile('setup.py'):
        process_setup_py('setup.py', BACKUP_SUFFIX)

    return 0

if __name__ == '__main__':
    sys.exit(main())
