# -*- coding: utf-8 -*-
import ast
import re

import pytest


class AnnotationRequirement:
    """Decorator requirement specification, read-only"""

    def __init__(self, required_by_dir_name, decorator_name):
        self.__name = decorator_name
        self.__required_by_dir_name = required_by_dir_name

    @property
    def name(self):
        return self.__name

    @property
    def required_by_dir_name(self):
        return self.__required_by_dir_name

    def __repr__(self):
        return (f'Required annotation "{self.name}" for each function/class '
                f'declaration under "/{self.required_by_dir_name}" directory')


PLUGIN_NAME = 'annotation-check'
DEFAULT_REQUIRED_ANNOTATIONS = [
    AnnotationRequirement('integration_tests', 'integration_test'),
]
TEST_CLASS_PREFIX = 'test'


def pytest_addoption(parser):
    group = parser.getgroup('general')
    group.addoption(
        f'--{PLUGIN_NAME}',
        dest=PLUGIN_NAME,
        action='store_true',
        help='Perform initial decorator checks',
    )


def pytest_sessionstart(session):
    """
    Checks whether there are custom specification of decorator requirements
    """
    config = session.config
    config.decorator_requirements = DEFAULT_REQUIRED_ANNOTATIONS


def pytest_collect_file(path, parent):
    config = parent.config
    if config.getoption(PLUGIN_NAME):
        required_annotations = []
        for r in config.decorator_requirements:
            rel_path = config.rootdir.bestrelpath(path)
            if re.match(r.required_by_dir_name, rel_path):
                required_annotations.append(r)
        if required_annotations:
            return AnnotationCheckItem(path, parent, required_annotations)


class AnnotationCheckError(Exception):
    """ Indicates error during annotation checks"""

    def __init__(self, path, missing_annotations):
        self.path = path
        self.missing_annotations = missing_annotations

    def get_message(self):
        msg = ''
        for line_num, violated_requirements in self.missing_annotations:
            msg += f'{self.path}:{line_num}: {violated_requirements}'
        return msg


class AnnotationCheckItem(pytest.Item, pytest.File):
    """Checks annotation (for classes and/or for functions)"""

    def __init__(self, path, parent, required_annotations):
        super().__init__(path, parent)
        self.add_marker(PLUGIN_NAME)
        self.required_annotations = required_annotations

    def runtest(self):
        checker = AnnotationChecker(self.fspath, self.required_annotations)
        missing_annotations = checker.check()
        if missing_annotations:
            raise AnnotationCheckError(str(self.fspath), missing_annotations)

    def repr_failure(self, excinfo):
        if excinfo.errisinstance(AnnotationCheckError):
            return excinfo.value.get_message()
        return super().repr_failure(excinfo)

    def reportinfo(self):
        return self.fspath, -1, PLUGIN_NAME


class AnnotationChecker(ast.NodeVisitor):
    def __init__(self, path, required_annotations):
        self.path = path
        self.missing_annotations = []
        self.required_annotations = required_annotations

    def check(self):
        self.missing_annotations = []
        with open(self.path, 'r') as src_code:
            ast_tree = ast.parse(src_code.read())
            self.visit(ast_tree)
        return self.missing_annotations

    def visit_ClassDef(self, node):
        self._check_missing_annotations(node)

    def visit_FunctionDef(self, node):
        self._check_missing_annotations(node)

    def _check_missing_annotations(self, node):
        if node.name.lower().startswith(TEST_CLASS_PREFIX):
            node_decorators = node.decorator_list
            for dec_requirement in self.required_annotations:
                if not any(decorator.id == dec_requirement.name for decorator in node_decorators):
                    self.missing_annotations.append((node.lineno, dec_requirement))
