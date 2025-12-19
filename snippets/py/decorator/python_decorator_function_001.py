from collections.abc import Callable, Iterable, Mapping
from typing import Any


def decorator(myfunc: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Iterable[Any], **kwargs: Mapping[Any, Any]):
        print('Wrapper Always Executed.')
        return myfunc(*args, **kwargs)

    print('FunctionDecorator Executed Once.')
    return wrapper


@decorator
def Speak(a: int | str) -> int | str:
    return a * 3


if __name__ == '__main__':
    print(Speak('Word '))
    print(Speak('Test '))
