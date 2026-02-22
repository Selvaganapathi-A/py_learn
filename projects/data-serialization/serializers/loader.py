# app/io/loaders.py
from typing import Any

from .plugin_registry import PluginRegistry

loaders: PluginRegistry[Any, str] = PluginRegistry[Any, str]()


def load(data: Any, plugin: str) -> str:
    return loaders.run(plugin, data)
