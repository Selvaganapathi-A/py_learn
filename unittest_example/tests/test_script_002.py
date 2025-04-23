from unittest import TestCase


class TestDivision(TestCase):

    def test_division(self):
        assert 1 / 2 == 0.5

    def test_division_raising_error(self):
        with self.assertRaises(ZeroDivisionError):
            assert 1 / 0 == float('inf')
