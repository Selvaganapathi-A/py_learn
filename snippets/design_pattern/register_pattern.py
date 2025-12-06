from collections.abc import Callable
from functools import wraps
from pprint import pprint
from typing import Any

_REGISTRY: dict[str, Callable[[Any], None]] = {}


def register_exporter(format: str):
    def decorator(function: Callable[[Any], None]):
        global _REGISTRY

        @wraps(function)
        def wrapper(data: Any):
            return function(data)

        _REGISTRY[format] = wrapper
        return wrapper

    return decorator


def export_data(data: Any, format: str):
    exporter_function = _REGISTRY.get(format)
    if exporter_function is None:
        raise ValueError('Exporter Not Registered.')
    return exporter_function(data)


@register_exporter('pdf')
def export_pdf(data: Any):
    print(f'PDF : {data}')


@register_exporter('csv')
def export_csv(data: Any):
    print(f'CSV : {data}')


@register_exporter('xml')
def export_xml(data: Any):
    print(f'XML : {data}')


@register_exporter('json')
def export_json(data: Any):
    print('JSON : ')
    pprint(
        data,
        indent=1,
        depth=3,
        compact=True,
        sort_dicts=False,
    )


def main():
    data = {
        'name': 'Bob',
        'age': 42,
        'place': 'scotpit',
        'zipcode': 35007,
        'gender': 'M',
    }
    export_data(data, 'pdf')
    export_data(data, 'csv')
    export_data(data, 'json')
    export_data(data, 'xml')
    #
    # below code raises ValueError
    # No exporter is registered.
    export_data(data, 'text')


if __name__ == '__main__':
    main()
