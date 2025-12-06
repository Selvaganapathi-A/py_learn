from rich import print

from ..registry import register


@register('scream')
def Scream(name: str):
    print(f'[red]{name.upper()}[/red]')
    return name.upper()
