from decimal import Decimal
from random import randint

from rich import print
from rich.highlighter import Highlighter
from rich.text import Text


class RainbowHighlighter(Highlighter):
    def highlight(self, text: Text):
        for index in range(len(text)):
            text.stylize(f'color({randint(16, 255)})', index, index + 1)


rainbow = RainbowHighlighter()
print(rainbow('I must not fear. Fear is the mind-killer.'))
print(
    (
        [
            1,
            846.98,
            Decimal('97.765764'),
            4,
            5,
            'mani',
            ('saradha stores', 'madurai'),
        ],
    )
)
