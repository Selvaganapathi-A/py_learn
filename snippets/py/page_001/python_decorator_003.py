from typing import Any, Callable, Iterable, Mapping


# Decorator
def decorator_factory(*factory_args: int,
                      **factory_kwargs: str) -> Callable[..., Any]:

    def decorator(function: Callable[..., Any]) -> Callable[..., Any]:

        def wrapper(*args: Iterable[Any], **kwargs: Mapping[Any, Any]) -> Any:
            return (function(factory_kwargs.get('a', '_^_')) +
                    function(*args, **kwargs) +
                    function(factory_kwargs.get('b', '_^_')))

        return wrapper

    return decorator


@decorator_factory(23, 43, 71, a='ghost', b='rider')
def say_name(name: str):
    return f'<name>{name}</name>'


if __name__ == '__main__':
    print(say_name('Kavya'))
    print(say_name('Meena'))
    print(say_name('Madhan'))
