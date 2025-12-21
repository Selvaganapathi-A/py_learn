from rich import print

from ..repository import register


@register('shout')
def shout(sentence: str):
    content: str = sentence.upper()
    color: str = 'red'
    print(f'[{color}]{content}...[/{color}]')
    return content
