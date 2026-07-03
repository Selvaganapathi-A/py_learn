from typing import Any

import toml

from .. import dumper, loader


@dumper.dumpers.register('toml')
def dump(data: Any) -> str:
    return toml.dumps(data)


@loader.loaders.register('toml')
def load(data: str) -> Any:
    return toml.loads(data)
