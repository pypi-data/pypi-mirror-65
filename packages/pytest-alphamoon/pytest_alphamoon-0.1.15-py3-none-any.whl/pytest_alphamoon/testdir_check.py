# -*- coding: utf-8 -*-
"""
NOTE:
    This plugin should have been based on pytest's test discovery, but since this requires
    analysis of gathered tests at different pytest stage, for now plugin implements own
    discovery, which reports failure each time when function / class / file
    contains 'test' token without being under tests/ directory
"""
import os
import re

import pytest

TEST_FILE_PATTERNS = [
    r'test[\w]*\.py',
    r'[\w]*test\.py',
]

PLUGIN_NAME = 'testdir-check'
TESTS_REQUIRED_TOKEN_INI = 'tests_required_token'
DEFAULT_TEST_REQUIRED_TOKEN = {
    'tests',
}


def pytest_addoption(parser):
    group = parser.getgroup('general')
    group.addoption(
        f'--{PLUGIN_NAME}',
        dest=PLUGIN_NAME,
        action='store_true',
        help='Perform initial tests placement checks')

    parser.addini(TESTS_REQUIRED_TOKEN_INI, type='linelist', help=(
        'Each line specifies a single directory name, under which test files are allowed'
    ))


def pytest_sessionstart(session):
    """
    # TODO:
    """
    config = session.config
    if config.getoption(PLUGIN_NAME):
        test_required_token = config.getini(TESTS_REQUIRED_TOKEN_INI)
        if test_required_token:
            config.test_required_token = test_required_token
        else:
            config.test_required_token = DEFAULT_TEST_REQUIRED_TOKEN


def pytest_collect_file(path, parent):
    config = parent.config
    filename = path.basename
    if config.getoption(PLUGIN_NAME) and any(
            re.match(pattern, filename) for pattern in config.test_required_token):
        rel_path = config.rootdir.bestrelpath(path)
        return TestdirCheckItem(path, parent, rel_path, config.test_required_token)


class TestdirCheckError(Exception):
    """ Indicates error during checks of placement of test functions . """

    def __init__(self, path, err_message):
        self.path = path
        self.err_message = err_message

    def get_message(self):
        return f'{self.path}: {self.err_message}'


class TestdirCheckItem(pytest.Item, pytest.File):

    def __init__(self, path, parent, rel_path, test_required_token):
        super().__init__(path, parent)
        self.rel_path = rel_path
        self.test_required_token = test_required_token
        self.add_marker(PLUGIN_NAME)

    def runtest(self):
        testdir_err = check_testdir(self.rel_path, self.test_required_token)

        if testdir_err:
            raise TestdirCheckError(self.fspath, testdir_err)

    def repr_failure(self, excinfo):
        if excinfo.errisinstance(TestdirCheckError):
            return excinfo.value.get_message()
        return super().repr_failure(excinfo)

    def reportinfo(self):
        return self.fspath, -1, PLUGIN_NAME


def check_testdir(rel_path, test_required_token):
    path_components = rel_path.split(os.sep)
    if any(test_required_token == component for component in path_components):
        return ''
    return f'Invalid test file placement'
