import time
from collections.abc import Callable
from typing import Any, Self


class LazyProperty:
    def __init__(self, function: Callable[[Any], Any]) -> None:
        self.function: Callable[[Any], Any] = function
        self.name = function.__name__
        self.storage_name = f'_{function.__name__}'

        print(self.name)
        print(self.storage_name)
        print(self.function)

    def __get__(self, instance: object | None, owner: type) -> Self | int:
        if instance is None:
            return self

        if hasattr(instance, self.storage_name):
            return getattr(instance, self.storage_name)

        value = self.function(instance)
        print('Computing...')
        setattr(instance, self.storage_name, value)

        return value

    # def __set__(self, instance: object | None, value: int) -> None:
    #     print("in setter of lazy property.")
    #     print(instance, value)
    #     instance.__dict__[self.storage_name] = value


class DeepThought:
    def __init__(self, values: tuple[int, ...]) -> None:
        self._values: tuple[int, ...] = values

    @LazyProperty
    def meaning_of_life(self) -> int:
        time.sleep(1)
        return sum(self._values)


if __name__ == '__main__':
    my_deep_thought_instance = DeepThought((1, 2, 3, 6, 7, 8, 15, 23, 37, 41))
    print('*' * 80)
    for i in range(5):
        print(i, my_deep_thought_instance.meaning_of_life)
    print('*' * 80)
    print('End of Program')
