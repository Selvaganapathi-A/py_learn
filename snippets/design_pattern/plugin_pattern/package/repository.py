import importlib
import os
import pkgutil
from collections.abc import Callable
from functools import wraps
from pathlib import Path

_Function = Callable[[str], str]
_REGISTRY: dict[str, _Function] = {}


def register(name: str) -> Callable[[_Function], _Function]:
    def decorator(function: _Function) -> _Function:
        global _REGISTRY
        nonlocal name

        @wraps(function)
        def wrapper(arg: str) -> str:
            return function(arg)

        _REGISTRY[name] = wrapper
        return wrapper

    return decorator


def execute(sentence: str, plugin: str) -> str:
    global _REGISTRY
    func: _Function | None = _REGISTRY.get(plugin)
    if func is None:
        raise KeyError(
            f'❌ Plugin "{plugin}" not Found!', tuple(_REGISTRY.keys())
        )
    return func(sentence)


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
