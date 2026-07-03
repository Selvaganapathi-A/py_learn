from rich import print

from ..repository import register


@register('scream')
def scream(sentence: str):
    """
    (str) -> str

    :param sentence: Description
    :type sentence: str
    """
    content: str = sentence.upper()
    color: str = 'blue'
    print(f'[{color}]{content}!?!?!?!?!?...[/{color}]')
    return content
