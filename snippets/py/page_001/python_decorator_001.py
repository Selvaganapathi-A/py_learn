from typing import Any, Callable, Iterable, Mapping


def FunctionDecorator(
    myfunc: Callable[..., Any]
) -> Callable[..., Any]:

    def Wrapper(*args: Iterable[Any], **kwargs: Mapping[Any, Any]):
        print("Wrapper Always Executed.")
        return myfunc(*args, **kwargs)

    print("FunctionDecorator Executed Once.")
    return Wrapper


@FunctionDecorator
def Speak(a: int | str) -> int | str:
    return a * 3


if __name__ == "__main__":
    print(Speak("Word "))
    print(Speak("Test "))
