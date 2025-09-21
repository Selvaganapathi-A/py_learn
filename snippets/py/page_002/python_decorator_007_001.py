from typing import Any, Callable, Iterable, Mapping


def PrimeDecorator(myfunc: Callable[[str | float], Any]) -> Callable[..., Any]:
    def PrimeWrapper(*args: Iterable[Any], **kwargs: Mapping[Any, Any]):
        print('Prime Wrapper Always Executed.')
        return myfunc(*args, **kwargs)

    print('Prime Decorator Executed Once.')
    return PrimeWrapper


def AlphaDecorator(myfunc: Callable[[str | float], Any]) -> Callable[..., Any]:
    def AlphaWrapper(*args: Iterable[str | float], **kwargs: Mapping[Any, Any]):
        print('Alpha Wrapper Always Executed.')
        return myfunc(*args, **kwargs)

    print('Alpha Decorator Executed Once.')
    return AlphaWrapper


@PrimeDecorator
@AlphaDecorator
def Speak(a: str | float) -> str | float:
    return a * 2


@AlphaDecorator
@PrimeDecorator
def write(a: str | float) -> str | float:
    return a * 2


if __name__ == '__main__':
    print(Speak('Word '))
    print(Speak('Test '))
    print(Speak('Study '))
    print()
    print(write('Tour'))
    print(write('To'))
    print(write('Toronto'))
