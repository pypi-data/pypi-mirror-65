# -*- coding: utf-8 -*-
import os

import pytest

PLUGIN_NAME = 'init-check'
INIT_FORBIDDEN_INI = 'init_forbidden_in'
INIT_FILENAME = '__init__.py'
DEFAULT_INIT_FORBIDDEN_IN = {
    'scripts',
    'notebooks',
}


def pytest_addoption(parser):
    group = parser.getgroup('general')
    group.addoption(
        f'--{PLUGIN_NAME}',
        dest=PLUGIN_NAME,
        action='store_true',
        help='Perform checks for __init__.py presence in certain forbidden folders')

    parser.addini(INIT_FORBIDDEN_INI, type='linelist', help=(
        'Each line specifies a single directory name, under which __init__.py files are forbidden'
    ))


def pytest_sessionstart(session):
    """
    Checks whether there are names of directories, where __init__.py is forbidden,
    given in pytest.ini.
    In the case of lack of the forbidden imports specification, error is raised.
    """
    config = session.config
    if config.getoption(PLUGIN_NAME):
        ini_forbidden_inits = config.getini(INIT_FORBIDDEN_INI)
        if ini_forbidden_inits:
            config.ini_forbidden_inits = ini_forbidden_inits
        else:
            config.ini_forbidden_inits = DEFAULT_INIT_FORBIDDEN_IN


def pytest_collect_file(path, parent):
    config = parent.config
    basename = os.path.basename(path.dirname)
    filename = path.basename
    if config.getoption(PLUGIN_NAME) and basename in config.ini_forbidden_inits:
        return InitCheckItem(path, parent, basename, filename)


class ForbiddenInitError(Exception):
    """ Indicates missing newline at the end of file. """

    def __init__(self, path, basename):
        self.path = path.dirname
        self.basename = basename

    def get_message(self):
        return f'{self.path}: {INIT_FILENAME} forbidden under {self.basename} directory'


class InitCheckItem(pytest.Item, pytest.File):

    def __init__(self, path, parent, basename, filename):
        super().__init__(path, parent)
        self.basename = basename
        self.filename = filename

        self.add_marker(PLUGIN_NAME)

    def runtest(self):
        if self.filename == INIT_FILENAME:
            raise ForbiddenInitError(self.fspath, self.basename)

    def repr_failure(self, excinfo):
        if excinfo.errisinstance(ForbiddenInitError):
            return excinfo.value.get_message()
        return super().repr_failure(excinfo)

    def reportinfo(self):
        return self.fspath, -1, PLUGIN_NAME
