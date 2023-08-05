# -*- coding: utf-8 -*-

__author__ = 'XQ'

import os
import pkgutil
import importlib
import functools


def iter_package(package, filter=lambda _name: True):
    """
    迭代某package下所有子module
    :param package:包名或者包"core.crypt"
    :param filter:过滤字段,如handler,service,model等
    """
    if not package:
        return
    if type(package) is not str:
        package_name = package.__name__
    else:
        package_name = package
    package_path = package_name.replace('.', os.path.sep)
    for _, name, is_package in pkgutil.iter_modules([package_path]):
        child_name = package_name + '.' + name
        if is_package:
            for _module in iter_package(child_name, filter=filter):
                yield _module
        else:
            if filter(name):
                yield importlib.import_module(child_name)


is_handler = lambda _name: _name.endswith('handler')
is_api = lambda _name: _name.endswith('controller') or _name.endswith('api')
is_rpc = lambda _name: _name.endswith('rpc')
is_model = lambda _name: _name.endswith('model')


def iter_packages(packages, filter=lambda _name: True):
    for package in packages:
        for _module in iter_package(package, filter):
            yield _module


iter_handler_packages = functools.partial(iter_packages, filter=is_handler)
iter_api_packages = functools.partial(iter_packages, filter=is_api)
iter_rpc_packages = functools.partial(iter_packages, filter=is_rpc)
iter_model_packages = functools.partial(iter_packages, filter=is_model)


def import_packages(packages):
    iter_handler = iter_packages(packages)
    return [item for item in iter_handler]


def import_handler_packages(packages):
    iter_handler = iter_handler_packages(packages)
    return [item for item in iter_handler]


def import_api_packages(packages):
    iter_api = iter_api_packages(packages)
    return [item for item in iter_api]


def import_rpc_packages(packages):
    iter_rpc = iter_rpc_packages(packages)
    return [item for item in iter_rpc]


def import_model_packages(packages):
    iter_model = iter_model_packages(packages)
    return [item for item in iter_model]
