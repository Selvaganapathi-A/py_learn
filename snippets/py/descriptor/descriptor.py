import typing


class Piece:
    """A Simple Descriptor."""

    def __set_name__(self, owner: type, name: str) -> None:
        print(f'\x1b[38;5;27m{owner=!r} {name=!r}\x1b[0m')
        self.owner = owner
        self.name = name
        self.storage_name = f'_{owner.__name__}.{name}'

    def __get__(self, instance: object | None, owner: type) -> typing.Self | str:
        """
        Called When attribute is accessed.

        Returns:
            Self | str
        """
        print(f'\x1b[38;5;214m__get__ {self.storage_name} called with {instance=!r} {owner=!r}.\x1b[0m\n')
        if hasattr(instance, self.storage_name):
            return getattr(instance, self.storage_name)

        return self

    def __set__(self, instance: object | None, value: str) -> None:
        """Called When new value is assigned to attribute."""
        print(f'\x1b[38;5;46m__set__ {self.storage_name} called with {instance=!r} {value=!r}.\x1b[0m\n')
        setattr(instance, self.storage_name, value)

    def __delete__(self, instance: object | None) -> None:
        print(f'\x1b[38;5;202m__delete__ {self.storage_name} called with {instance=!r}.\x1b[0m\n')
        # del self.value
        print(instance.__dict__)
        delattr(instance, self.storage_name)
        print(instance.__dict__)


class Artifact:
    "Demo Class"

    x: Piece = Piece()
    y: Piece = Piece()


def main() -> None:
    artifact = Artifact()
    # interospect
    print(Artifact.x)
    # read from descriptor
    print(artifact.x)
    # set new value
    artifact.x = 'Golden Water.'

    print(artifact.x)

    print(type(artifact).__dict__['x'].__get__(artifact, type(artifact)))

    del artifact.x

    print(artifact.x)
    print(artifact.y)

    artifact.x = 'Polar beer.'

    print(artifact.x)

    print(type(artifact).__dict__)
    print(artifact.__dict__)


if __name__ == '__main__':
    main()
