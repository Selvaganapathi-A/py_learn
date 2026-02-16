from unittest import TestCase


class TestDivision(TestCase):
    def setUp(self):
        self.divider = 2
        return super().setUp()

    def test__division(self):
        result = 0.5
        assert result == 1 / self.divider

    def test__division_raising_error(self):
        with self.assertRaises(ZeroDivisionError):
            assert float("inf") == 1 / 0
