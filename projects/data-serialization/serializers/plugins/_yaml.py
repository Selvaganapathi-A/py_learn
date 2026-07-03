from pathlib import Path
from typing import Any

import yaml

from .. import dumper, loader


def path_representer(
    dumper: yaml.Dumper | yaml.SafeDumper,
    obj: Path,
) -> yaml.Node:
    return dumper.represent_scalar('!Path', str(obj))


def path_constructer(
    loader: yaml.Loader | yaml.FullLoader | yaml.UnsafeLoader | yaml.SafeLoader,
    node: yaml.Node | yaml.ScalarNode | yaml.MappingNode,
) -> Any:
    data = loader.construct_scalar(node)  # pyright: ignore[reportArgumentType]
    return Path(data)


@dumper.dumpers.register('yaml')
def dump(data: Any) -> str:
    return yaml.safe_dump(
        data,
        indent=4,
        allow_unicode=True,
        line_break='\n',
        width=80,
        sort_keys=False,
    )


@loader.loaders.register('yaml')
def load(data: str) -> Any:
    return yaml.load(data, yaml.SafeLoader)


yaml.add_representer(Path, path_representer)
yaml.add_constructor('!Path', path_constructer)
