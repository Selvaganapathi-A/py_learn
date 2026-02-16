import secrets


class Sensor:
    @property
    def temperature(self) -> int:
        return secrets.choice(range(10, 45))
