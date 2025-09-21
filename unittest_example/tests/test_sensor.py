from unittest import TestCase, mock

from py_learn.unittest_example.alarm import Alarm
from py_learn.unittest_example.sensor import Sensor
from py_learn.unittest_example.testsensor import TestSensor


class TestAlarm(TestCase):
    def test_alarm_is_off_by_default(self):
        alarm: Alarm = Alarm()
        alarm.check()
        assert alarm.is_on

    def test_temperature_is_too_high(self):
        alarm = Alarm(TestSensor(25))
        alarm.check()
        assert alarm.is_on

    def test_temperature_is_too_low(self):
        alarm = Alarm(TestSensor(25))
        alarm.check()
        assert alarm.is_on

    def test_temperature_is_normal(self):
        alarm = Alarm(TestSensor(20))
        alarm.check()
        self.assertFalse(alarm.is_on)

    @mock.patch('py_learn.unittest_example.sensor.Sensor')
    def test_temperature_is_too_low_002(self, sensor: mock.MagicMock):
        sensor.temperature = 25
        alarm = Alarm(sensor)
        alarm.check()
        assert alarm.is_on


class TestAlarm002(TestCase):
    def setUp(self):
        self.mock_sensor: mock.MagicMock = mock.MagicMock(Sensor)
        self.alarm = Alarm(self.mock_sensor)

    def test_alarm_is_off_by_default(self):
        alarm = Alarm()
        self.assertFalse(alarm.is_on)

    def test_check_temperature_too_high(self):
        self.mock_sensor.temperature = 25
        self.alarm.check()
        self.assertTrue(self.alarm.is_on)

    def test_check_temperature_too_low(self):
        self.mock_sensor.temperature = 15
        self.alarm.check()
        self.assertTrue(self.alarm.is_on)

    def test_check_normal_temperature(self):
        self.mock_sensor.temperature = 20
        self.alarm.check()
        self.assertFalse(self.alarm.is_on)

    def tearDown(self) -> None:
        del self.mock_sensor, self.alarm
