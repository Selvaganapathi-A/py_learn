import os
from pprint import pformat

from icecream import ic

ic.configureOutput(
    argToStringFunction=lambda obj: pformat(
        obj,
        indent=4,
        width=os.get_terminal_size().columns,
        sort_dicts=False,
        depth=4,
    ),
)

x = {'hi': 2, 'hello': 5, 'pear': 4, 'jaguar': {'lion': 4, 'kangaroo': 2}}


ic(x)
