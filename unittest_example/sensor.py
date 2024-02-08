import random


class Sensor:

    @property
    def temperature(self) -> int:
        return random.randint(10, 45)
