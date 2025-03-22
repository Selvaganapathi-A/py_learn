from pprint import pformat

from icecream import ic

ic.configureOutput(
    argToStringFunction=lambda obj: pformat(
        obj,
        indent=2,
        width=78,
        sort_dicts=False,
    ),
)
