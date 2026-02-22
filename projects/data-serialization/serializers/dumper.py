# app/io/dumpers.py
from typing import Any

from .plugin_registry import PluginRegistry

dumpers: PluginRegistry[Any, str | bytes] = PluginRegistry[Any, str | bytes]()


def dump(data: Any, plugin: str) -> str | bytes:
    return dumpers.run(plugin, data)
