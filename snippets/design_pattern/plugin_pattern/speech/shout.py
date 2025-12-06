from rich import print

from ..registry import register


@register('shout')
def Shout(name: str):
    print((f'[cyan][bold]{name.upper()}!![/cyan]'))
    return name.upper()
