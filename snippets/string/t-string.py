from string.templatelib import Interpolation, Template, convert


def convert_to_string(arg: str | Interpolation) -> str:
    match arg:
        case str():
            return arg
        case Interpolation(value, expression, conversion, format_specifier):  # noqa: F841
            return format(convert(value, conversion), format_specifier)
        case _:
            raise NotImplementedError()


def build_string(text: Template) -> str:
    txt = []
    for string in text:
        txt.append(convert_to_string(string))
    return ''.join(txt)


def main():
    business: str = 'cafè'
    health: float = 93.7
    blessing: str = 'kudos'
    feeling: str = '😊'
    # define template string
    string_template = t'Hello [{health: ^14.3f}] {business!a} {blessing!r} {feeling!s} [{health!s: >8s}]'
    #  build string when needed.
    print(build_string(string_template))


if __name__ == '__main__':
    main()

# __match_args__ = ('value', 'expression', 'conversion', 'format_spec')
