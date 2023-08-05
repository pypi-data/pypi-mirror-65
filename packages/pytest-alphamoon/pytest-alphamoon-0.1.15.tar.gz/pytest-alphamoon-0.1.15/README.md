# pytest-alphamoon

[![image](https://img.shields.io/pypi/v/pytest-alphamoon.svg)](https://pypi.org/project/pytest-alphamoon%0A%20:alt:%20PyPI%20version)
[![image](https://img.shields.io/pypi/pyversions/pytest-alphamoon.svg)](https://pypi.org/project/pytest-alphamoon)

Set of simple static code checks at Alphamoon.

* * * * *

This [pytest](https://github.com/pytest-dev/pytest) plugin was generated
with [Cookiecutter](https://github.com/audreyr/cookiecutter) along with
[@hackebrot](https://github.com/hackebrot)'s
[cookiecutter-pytest-plugin](https://github.com/pytest-dev/cookiecutter-pytest-plugin)
template. Source code is based on [pytest-isort](https://github.com/moccu/pytest-isort) plugin.

Features
--------

Package contains several plugins, as shown in Table below:


| Plugin         | Description           |
| -------------- | --------------------- |
| [import-check](pytest_alphamoon/import_check.py) | Checks no imports from `scripts`/`notebooks`/`user_settings`|
| [init-check](pytest_alphamoon/init_check.py) | Checks no `__init__.py` file in `scripts`/`notebooks`|
| [notebook-check](pytest_alphamoon/notebook_check.py) | Checks notebooks (`.ipnyb` files) are clean, without outputs || [notebook-check](pytest_alphamoon) | Checks notebooks (`.ipnyb` files) are clean, without outputs | 
| [newline-check](pytest_alphamoon/newline_check.py) | Checks files (`requirements*`, `.gitignore` or custom) for newline at the end of file |  
| [testdir-check](pytest_alphamoon/testdir_check.py) | Checks test files (files matching patterns: `test_*.py` or `*_test.py`) are under `/tests` directory |
| [annotation-check](pytest_alphamoon/annotation_check.py) | Checks integration tests function/class definition (all class and functions defined under `integration_tests` prefixed with `test*`) has decorator `@integration_test` |

Requirements
------------
```requirements.txt
pytest>=3.5.0
```

Installation
------------

You can install "pytest-alphamoon" via
[pip](https://pypi.org/project/pip/) from
[PyPI](https://pypi.org/project):

    $ pip install pytest-alphamoon

Usage
-----

You can add arbitrary plugin from this package by specifying its name in `pytest.ini` `addopts`
section with plugin names as shown in Table above along with any other plugin you are currently using.

```ini
[pytest]
addopts = --init-check --import-check --notebook-check  --newline-check --testdir-check
          --annotation-check

import_forbidden_from =
    scripts
    user_settings
    notebooks

notebook_allowed_in =
    notebooks

init_forbidden_in =
    scripts
    notebooks
``` 

**Parameters, like `import_forbidden_from`, shown in example configuration above are optional. 
If custom values are not provided in `pytest.ini` file, default parameters are used.**


After setting up configuration file specified checks are loaded and executed automatically within test session, 
after invoking command:

    $ pytest

Contributing
------------

Contributions are very welcome. Tests can be run with
[tox](https://tox.readthedocs.io/en/latest/), please ensure the coverage
at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the
[MIT](http://opensource.org/licenses/MIT) license, "pytest-alphamoon" is
free and open source software

Issues
------

If you encounter any problems, please email us at <dev@alphamoon.ai>, along with a detailed description.
