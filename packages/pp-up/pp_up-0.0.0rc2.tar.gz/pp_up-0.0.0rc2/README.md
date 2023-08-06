pp-up
=====

Overview
--------
Script to update your dependencies by checking if there are new versions
available on pypi.

This script parses your requirements.txt and setup.py files, and updates any
pinned version you may have to the latest version available on pypi.

This script is fairly dumb, so if you have pinned a version for a specific
reason, you still have to apply some logic to the result.

The files are backupped before modification.

Usage
-----
```bash
cd $YOUR_PROJECT_DIR
python -m pp_up
```
