import secrets
from unittest import TestCase, mock

from py_learn.unittest_example import odometer
"""


When to use mock
These are cases that you may consider using mocks:

System calls

-> Networking
-> I/O operation
-> Clocks & time, timezones
-> Or other cases whose results are unpredictable
-> Why using mocks


The following are benefits of mocks:

-> Speed up the test
-> Exclude external redundancies
-> Make unpredictable results predictable

"""


class Test_odometer(TestCase):

    def test_low_speed(self):
        odometer.speed = mock.Mock()
        odometer.speed.return_value = 20
        assert odometer.alert() == "slow"
        self.assertEqual(odometer.alert(), "slow")

    def test_normal_speed(self):
        odometer.speed = mock.Mock()
        odometer.speed.return_value = 40
        assert odometer.alert() == "normal"
        self.assertEqual(odometer.alert(), "normal")

    def test_high_speed(self):
        odometer.speed = mock.Mock()
        odometer.speed.return_value = 72
        assert odometer.alert() == "high"
        self.assertEqual(odometer.alert(), "high")

    def test_dangerous_speed(self):
        odometer.speed = mock.Mock()
        odometer.speed.return_value = 90
        assert odometer.alert() == "dangerous"
        self.assertEqual(odometer.alert(), "dangerous")


class Test_builtins_Secrets(TestCase):

    def test_mocking_builtin_secrets_module(self):
        secrets.choice = mock.Mock()
        secrets.choice.return_value = 900
        self.assertEqual(secrets.choice([900, 100, 500]), 900)
