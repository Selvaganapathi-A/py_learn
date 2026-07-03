from typing import Any

import orjson

from .. import dumper, loader
from ..helper import normalize


@dumper.dumpers.register('orjson')
def dump(data: Any) -> bytes:
    return orjson.dumps(data, default=normalize, option=orjson.OPT_INDENT_2)


@loader.loaders.register('orjson')
def load(data: bytes) -> Any:
    return orjson.loads(data)
