from typing import Protocol, Self, cast


class LightState(Protocol):
    def switch(self, bulb: "LightBulb"): ...
    def show(self): ...


class OffState:
    __instance__: Self | None = None

    def __new__(cls: type[Self]) -> Self:
        if cls.__instance__ is None:
            cls.__instance__ = super().__new__(cls)
        return cast(Self, cls.__instance__)

    def switch(self, bulb: "LightBulb"):
        bulb.state = OnState()
        print("Light is on -> off")

    def show(self):
        print("Light is Off.")


class OnState:
    __instance__: Self | None = None

    def __new__(cls: type[Self]) -> Self:
        if cls.__instance__ is None:
            cls.__instance__ = super().__new__(cls)
        return cast(Self, cls.__instance__)

    def switch(self, bulb: "LightBulb"):
        bulb.state = OffState()
        print("Light is off -> on")

    def show(self):
        print("Light is On.")


class LightBulb:
    def __init__(self) -> None:
        self.state: LightState = OffState()

    def switch(self):
        self.state.switch(self)


def main():
    bulb = LightBulb()
    bulb.switch()
    bulb.switch()
    bulb.switch()
    bulb.switch()
    print()
    bulb.state.show()
    bulb.state.show()


if __name__ == "__main__":
    main()
