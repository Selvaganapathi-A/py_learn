import time
from typing import Any, Callable


class Factory:

    def __init__(
        self,
        *factory_args: int,
        **factory_kwargs: str,
    ) -> None:
        print(factory_args)
        print(factory_kwargs)

    def __call__(self, function: Callable[..., Any]) -> Any:

        def wrapper(*args: Any, **kwargs: Any):
            print(args, kwargs)
            start: int = time.perf_counter_ns()
            result: Any = function(*args, **kwargs)
            end: int = time.perf_counter_ns()
            print(f"{end - start} nano seconds take to run.")
            return result

        return wrapper


@Factory(1, 2, 3, a="z", b="y", c="x", d="w")
def sayname(name: str):
    return (" " + name + " ") * 4


if __name__ == "__main__":
    print()
    print(sayname("google"))
    print()
    print(sayname("bing"))
    print()
    print(sayname("yahoo"))
    print()
    pass
