from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


class PluginRegistry[I, O]:
    def __init__(self) -> None:
        self._registry: dict[str, Callable[[I], O]] = {}

    def register(self, name: str) -> Callable[[Callable[[I], O]], Callable[[I], O]]:
        def decorator(fn: Callable[[I], O]) -> Callable[[I], O]:
            if name in self._registry:
                error_message = f"Plugin '{name}' already registered"
                raise ValueError(error_message)

            self._registry[name] = fn
            return fn

        return decorator

    def get(self, name: str) -> Callable[[I], O]:
        try:
            return self._registry[name]
        except KeyError:
            error_message = f"Plugin '{name}' is not registered"
            raise ValueError(error_message) from None

    def run(self, name: str, arg: I) -> O:
        return self.get(name)(arg)

    def available(self) -> list[str]:
        return sorted(self._registry)
