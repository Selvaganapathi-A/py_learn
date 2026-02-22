from typing import Any

import ujson

from .. import dumper, loader


@dumper.dumpers.register("ujson")
def dump(data: Any) -> str:
    return ujson.dumps(data)


@loader.loaders.register("ujson")
def load(data: str) -> Any:
    return ujson.loads(data)
