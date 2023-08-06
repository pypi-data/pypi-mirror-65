# -*- coding: utf-8 -*-
import json

import pytest

PLUGIN_NAME = 'notebook-check'
NOTEBOOK_ALLOWED_INI = 'notebook_allowed_in'
JUPYTER_NOTEBOOK = '.ipynb'
DEFAULT_NOTEBOOK_ALLOWED = {
    'notebooks',
}


def pytest_addoption(parser):
    group = parser.getgroup('general')
    group.addoption(
        f'--{PLUGIN_NAME}',
        dest=PLUGIN_NAME,
        action='store_true',
        help='Perform checks whether notebooks has been cleaned'
             ' and are placed under proper (specified) directory')

    parser.addini(NOTEBOOK_ALLOWED_INI, type='linelist', help=(
        'Each line specifies a single directory name, under which jupyter notebooks might be placed'
    ))


def pytest_sessionstart(session):
    """
    Checks whether in pytest.ini directory names, where jupyter notebooks are allowed, was provided
    In the case of lack of the notebooks directory names specification, error is raised.
    """
    config = session.config
    if config.getoption(PLUGIN_NAME):
        ini_allowed_notebook_dirs = config.getini(NOTEBOOK_ALLOWED_INI)
        if ini_allowed_notebook_dirs:
            config.ini_allowed_notebook_dirs = ini_allowed_notebook_dirs
        else:
            config.ini_allowed_notebook_dirs = DEFAULT_NOTEBOOK_ALLOWED


def pytest_collect_file(path, parent):
    config = parent.config
    if config.getoption(PLUGIN_NAME) and path.ext == JUPYTER_NOTEBOOK:
        return NotebookCheckItem(path, parent)


def check_notebook_dir(path, allowed_dirs):
    if not any(name in path.strpath for name in allowed_dirs):
        return f'notebook not under one of allowed directories: {allowed_dirs}'
    return ''


def check_notebook_output(path):
    with open(path, 'r') as notebook_file:
        notebook = json.load(notebook_file)
        for cell in notebook['cells']:
            if (cell.get('ExecuteTime') is not None or
                    cell.get('execution_count') is not None or
                    cell.get('outputs')):
                return 'notebook with output'
    return ''


class NotebookCheckError(Exception):
    """ Indicates incorrect .ipnyb file placement. """

    def __init__(self, path, error_messages):
        self.path = path
        self.error_messages = error_messages

    def get_message(self):
        return f'{self.path}: {", ".join(self.error_messages)}\n'


class NotebookCheckItem(pytest.Item, pytest.File):

    def __init__(self, path, parent):
        super().__init__(path, parent)
        self.add_marker(PLUGIN_NAME)

    def runtest(self):
        error_messages = []
        dir_error = check_notebook_dir(self.fspath, self.config.ini_allowed_notebook_dirs)
        if dir_error:
            error_messages.append(dir_error)

        output_error = check_notebook_output(self.fspath)
        if output_error:
            error_messages.append(output_error)

        if error_messages:
            raise NotebookCheckError(str(self.fspath), error_messages)

    def repr_failure(self, excinfo):
        if excinfo.errisinstance(NotebookCheckError):
            return excinfo.value.get_message()
        return super().repr_failure(excinfo)

    def reportinfo(self):
        return self.fspath, -1, PLUGIN_NAME
