from collections.abc import Callable, Mapping
from typing import Any


def PrimeDecorator(myfunc: Callable[[str | float], Any]) -> Callable[..., Any]:
    def PrimeWrapper(*args: str | float, **kwargs: Mapping[Any, Any]):
        print('Prime Wrapper Always Executed.')
        return myfunc(*args, **kwargs)

    print('Prime Decorator Executed Once.')
    return PrimeWrapper


def AlphaDecorator(myfunc: Callable[[str | float], Any]) -> Callable[..., Any]:
    def AlphaWrapper(*args: str | float, **kwargs: Mapping[Any, Any]):
        print('Alpha Wrapper Always Executed.')
        return myfunc(*args, **kwargs)

    print('Alpha Decorator Executed Once.')
    return AlphaWrapper


@PrimeDecorator
@AlphaDecorator
def Speak(a: str | float) -> str | float:
    # -- decorator order
    # 1. AlphaDecorator
    # 2. PrimeDecorator
    return a * 2


@AlphaDecorator
@PrimeDecorator
def write(a: str | float) -> str | float:
    return a * 2


if __name__ == '__main__':
    print(Speak('Word '))
    print(Speak('Test '))
    print(Speak('Study '))
    print(write('Tour'))
    print(write('To'))
    print(write('Toronto'))
