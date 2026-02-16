from unittest import TestCase, mock

from py_learn.unittest_example.alarm import Alarm
from py_learn.unittest_example.dummysensor import DummySensor
from py_learn.unittest_example.sensor import Sensor


class TestAlarm(TestCase):
    def setUp(self):
        self.alarm: Alarm = Alarm()
        self.alarm_high = Alarm(DummySensor(25))
        self.alarm_low = Alarm(DummySensor(10))
        self.alarm_normal = Alarm(DummySensor(20))

    def test__alarm_is_off_by_default(self):
        self.alarm.check()
        assert self.alarm.is_on

    def test__temperature_is_too_high(self):
        self.alarm_high.check()
        assert self.alarm_high.is_on

    def test__temperature_is_too_low(self):
        self.alarm_low.check()
        assert self.alarm_low.is_on

    def test__temperature_is_normal(self):
        self.alarm_normal.check()
        self.assertFalse(self.alarm_normal.is_on)

    @mock.patch("py_learn.unittest_example.sensor.Sensor")
    def test__temperature_is_too_low_002(self, sensor: mock.MagicMock):
        sensor.temperature = 25
        self.alarm.check()
        assert self.alarm.is_on is True


class TestAlarm002(TestCase):
    def setUp(self):
        self.mock_sensor: mock.MagicMock = mock.MagicMock(Sensor)
        self.alarm = Alarm(self.mock_sensor)

    def test__alarm_is_off_by_default(self):
        alarm = Alarm()
        self.assertFalse(alarm.is_on)

    def test__check_temperature_too_high(self):
        self.mock_sensor.temperature = 25
        self.alarm.check()
        self.assertTrue(self.alarm.is_on)

    def test__check_temperature_too_low(self):
        self.mock_sensor.temperature = 15
        self.alarm.check()
        self.assertTrue(self.alarm.is_on)

    def test__check_normal_temperature(self):
        self.mock_sensor.temperature = 20
        self.alarm.check()
        self.assertFalse(self.alarm.is_on)

    def tearDown(self) -> None:
        del self.mock_sensor, self.alarm
