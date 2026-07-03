from rich import print

from ..repository import register


@register('whisper')
def whisper(sentence: str):
    content: str = sentence.capitalize()
    color: str = 'cyan'
    print(f'[{color}]{content}[/{color}]')
    return content
