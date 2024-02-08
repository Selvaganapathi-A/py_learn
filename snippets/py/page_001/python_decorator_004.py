from typing import Any, Callable

import time


class decorate:
    def __init__(self, function: Callable[..., Any]) -> None:
        self.function: Callable[..., Any] = function

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        start: int = time.perf_counter_ns()
        result: Any = self.function(*args, **kwargs)
        end: int = time.perf_counter_ns()
        print(f"{end - start} nano seconds take to run.")
        return result


@decorate
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
