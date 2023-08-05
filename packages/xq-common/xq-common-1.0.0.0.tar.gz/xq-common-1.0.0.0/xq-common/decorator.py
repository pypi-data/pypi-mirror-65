# -*- coding: utf-8 -*-

__author__ = 'XQ'

import functools
import inspect
import re


def under_score_case(camel_case):
    if not camel_case:
        return ""
    return re.compile('([^A-Z])([A-Z])').sub(r"\1_\2", camel_case).lower()


class Decorator:
    def get_modules(self):
        if not self.__dict__.get("modules"):
            self.modules = {}
        return self.modules

    def module(self, module):
        modules = self.get_modules()
        stack = inspect.stack()
        cls = stack[1][3]
        is_class = cls != "<module>"
        _module = stack[1][0].f_locals.get("__module__" if is_class else "__name__")
        name = module

        def decorator(origin):
            metas = modules.get(_module)
            if metas:
                del modules[_module]
                modules[under_score_case(name)] = metas

            @functools.wraps(origin)
            def wrapper(*args, **kw):
                return origin(*args, **kw)

            return wrapper

        if isinstance(module, str):
            return decorator
        else:
            name = module.__name__
            return decorator(module)

    def action(self, action):
        modules = self.get_modules()
        stack = inspect.stack()
        cls = stack[1][3]
        is_class = cls != "<module>"
        _module = stack[1][0].f_locals.get("__module__" if is_class else "__name__")
        name = action

        def decorator(origin):
            @functools.wraps(origin)
            def wrapper(*args, **kw):
                return origin(*args, **kw)

            _meta = {
                "action": under_score_case(name),
                "module": _module,
                "method": origin.__name__,
            }
            if is_class:
                _meta["class"] = cls
            metas = modules.get(_module)
            if not metas:
                metas = []
                modules[_module] = metas
            params = list(origin.__code__.co_varnames)
            if is_class:
                _meta["class"] = cls
            if len(params) > 1 or not is_class and len(params) > 0:
                _meta["params"] = params
            metas.append(_meta)
            _doc = inspect.getdoc(origin)
            _description = _doc.split("\n")[0] if _doc else ""
            wrapper.__description__ = _description
            return wrapper

        if isinstance(action, str):
            return decorator
        name = action.__name__
        return decorator(action)
