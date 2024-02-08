from typing import Any, Callable, Iterable, Mapping


# Decorator
def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args: Iterable[Any], **kwargs: Mapping[Any, Any]) -> Any:
        wrapper.called += 1
        return function(*args, **kwargs)

    wrapper.called = 0
    return wrapper


@decorator
def say_name(name: str):
    print(f"<{name.lower()}> {name.upper()} </{name.lower()}>")


if __name__ == "__main__":
    say_name("Kavya")
    print(say_name.called)
    print()
    say_name("Ganga")
    print(say_name.called)
    print()
    say_name("Yamuna")
    print(say_name.called)
    print()
    say_name("Arun")
    print(say_name.called)
    print()
    say_name("Maadhavan")
    print(say_name.called)
    print()
    pass
