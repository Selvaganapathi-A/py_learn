from collections.abc import Callable
from string.templatelib import Interpolation, Template, convert


def build_template(text: Template, apply: Callable[[str], str]):
    values: list[str] = []
    for var in text:
        if isinstance(var, str):
            values.append(var)
        else:
            values.append(apply(var.value))
    return ''.join(values)


def render_to_string(text: Template):
    values: list[str] = []
    for var in text:
        match var:
            case str():
                values.append(var)
            case Interpolation(value, expression, conversion, format_specifier):
                txt = convert(value, conversion)
                if format_specifier:
                    txt = format(txt, format_specifier)
                values.append(txt)
            case _:
                raise ValueError()
    return ''.join(values)


def main():
    name: str = 'Guava'
    price: float = 12.54354
    #
    t_string: Template = t'Product = {name!r}, price = {price: >10.2f}.'
    text = render_to_string(t_string)
    #
    print()
    print(t_string)
    print()
    print(text)
    print()


if __name__ == '__main__':
    main()
