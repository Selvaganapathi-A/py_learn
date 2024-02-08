class TestSensor:

    def __init__(self, temperature: int) -> None:
        self._temperature = temperature

    @property
    def temperature(self):
        return self._temperature
