#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions to handle Python modules
"""

from __future__ import print_function, division, absolute_import

import os
import sys
import imp
import inspect
import importlib

from tpDcc.libs import python
from tpDcc.libs.python import path as path_utils


def is_dotted_module_path(module_path):
    """
    Returns whether given module path is a dotted one (tpDcc.libs.python.modules) or not
    :param module_path: str
    :return: bool
    """

    return len(module_path.split('.')) > 2


def convert_to_dotted_path(path):
    """
    Returns a dotted path relative to the given path
    :param path: str, (eg. randomPath/folder/test.py)
    :return: str, dotted path (eg. folder.test)
    """

    directory, file_path = os.path.split(path)
    directory = path_utils.clean_path(directory)
    file_name = os.path.splitext(file_path)[0]
    package_path = [file_name]
    sys_path = [path_utils.clean_path(p) for p in sys.path]
    drive_letter = os.path.splitdrive(path)[0] + '\\'
    while directory not in sys_path:
        directory, name = os.path.split(directory)
        directory = path_utils.clean_path(directory)
        if directory == drive_letter or name == '':
            return ''
        package_path.append(name)

    return '.'.join(reversed(package_path))


def import_module(module_path, name=None):
    """
    Imports the given module path. If the given module path is a dotted one, import lib will be used. Otherwise, it's
    expected that given module path is the absolute path to the source file. If name argument is not given, then the
    basename without the extension will be used
    :param module_path: str, module path. Can be a dotted path (tpDcc.libs.python.modules) or an absolute one
    :param name: str, name for the imported module which will be used if the module path is an absolute path
    :return: ModuleObject, imported module object
    """

    if is_dotted_module_path(module_path) and not os.path.exists(module_path):
        try:
            return importlib.import_module(module_path)
        except ImportError:
            python.logger.error('Failed to load module: "{}"'.format(module_path), exc_info=True)

    try:
        if os.path.exists(module_path):
            if not name:
                name = os.path.splitext(os.path.basename(module_path))[0]
            if name in sys.modules:
                return sys.modules[name]
        if os.path.isdir(module_path):
            module_path = os.path.join(module_path, '__init__.py')
            if not os.path.exists(module_path):
                raise ValueError('Cannot find module path: "{}"'.format(module_path))
        return imp.load_source(name, os.path.realpath(module_path))
    except ImportError:
        python.logger.error('Failed to load module: "{}"'.format(module_path))
        raise


def iterate_modules(path, exclude=None):
    """
    Iterates all the modules of the given path
    :param path: str, folder path to iterate
    :param exclude: list(str), list of files to exclude
    :return: iterator
    """

    if not exclude:
        exclude = list()

    _exclude = ['__init__.py', '__init__.pyc']
    for root, dirs, files in os.walk(path):
        if '__init__.py' not in files:
            continue
        for f in files:
            base_name = os.path.splitext(f)[0]
            if f not in _exclude and base_name not in exclude:
                module_path = os.path.join(root, f)
                if f.endswith('.py') or f.endswith('.pyc'):
                    yield module_path


def iterate_module_members(module_to_iterate, predicate=None):
    """
    Iterates all the members of the given modules
    :param module_to_iterate: ModuleObject, module object to iterate members of
    :param predicate: inspect.cass, if given members will be restricted to given inspect class
    :return: iterator
    """

    for mod in inspect.getmembers(module_to_iterate, predicate=predicate):
        yield mod


def iterate_module_subclasses(module, class_type):
    """
    Iterates all classes within a module object returning all subclasses of given type
    :param module: ModuleObject, module object to iterate subclasses of
    :param class_type: object, class object to find
    :return: generator(object), generator function returning class objects
    """

    for member in iterate_module_members(module, predicate=inspect.isclass):
        if issubclass(member, class_type):
            yield member
