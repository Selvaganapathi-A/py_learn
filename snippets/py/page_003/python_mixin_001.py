import typing
from dataclasses import dataclass

import json5


class SerializerProtocol(typing.Protocol):
    def serislize(self): ...


class Serializer:
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

    def serialize(self):
        return {'args': self.args, **self.kwargs}


class Device(Serializer): ...


class Jsonizer:
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs

    def json(self: SerializerProtocol):
        return json5.dumps(self.serialize(), sort_keys=True)


@dataclass
class iPod(Device, Jsonizer):
    def __init__(self, *args, spicies='Monkey', **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.spicies = spicies


if __name__ == '__main__':
    iDevice = iPod(
        14,
        'en-US',
        OS='mountain-lion',
        Owner='tim cook',
        Head_Office='San Andreas',
    )
    print(iDevice)
    print(iDevice.serialize())
    ddata = iDevice.json()
    print(ddata)
    print(json5.loads(ddata))
