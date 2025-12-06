import importlib
import os
import pkgutil
from collections.abc import Callable
from functools import wraps
from pathlib import Path
from typing import Any

FUNCTION = Callable[..., Any]
_REGISTRY: dict[str, FUNCTION] = {}


def register(name: str) -> FUNCTION:
    def decorator(function: FUNCTION) -> FUNCTION:
        global _REGISTRY
        nonlocal name

        @wraps(function)
        def wrapper(*args, **kwargs) -> Any:
            return function(*args, **kwargs)

        _REGISTRY[name] = wrapper
        return wrapper

    return decorator


def execute(name: str, *args, **kwargs):
    global _REGISTRY
    func = _REGISTRY.get(name)
    if func is None:
        raise KeyError(f'❌ Plugin "{name}" not Found!')
    return func(*args, *kwargs)


def load_all_modules_in_this_package(args: list[str], level: int = 0):
    sub_packages: list[str] = []
    package_name = args[0].rsplit(os.sep, 1)[-1]
    module_name = (__name__.rsplit('.', 1))[0]
    # print(args, f'{module_name}.{package_name}')
    for _, x, _y in pkgutil.iter_modules(args):
        loader_arg = f'{module_name}.{package_name}.{x}'
        if level > 0:
            importlib.import_module(loader_arg)
            # print(loader_arg)
        if _y:
            sub_packages.append(args[0] + os.sep + x)
    for package in sub_packages:
        load_all_modules_in_this_package([package], level + 1)


load_all_modules_in_this_package([str(Path(__file__).parent)])
