from rich import print

from ..registry import register


@register('whisper')
def whisper(name: str):
    print(f'[black]{name}[/black]')
