from typing import Protocol

from py_learn.unittest_example.sensor import Sensor


class Temperature_Sensor(Protocol):

    @property
    def temperature(self) -> int:
        return 1


class Alarm:

    def __init__(self, sensor: Temperature_Sensor | None = None) -> None:
        self._low: int = 18
        self._high: int = 24
        self._sensor: Temperature_Sensor = sensor or Sensor()
        self._is_on: bool = False

    def check(self):
        temperature: int = self._sensor.temperature
        if temperature < self._low or temperature > self._high:
            self._is_on = True

    @property
    def is_on(self) -> bool:
        return self._is_on
