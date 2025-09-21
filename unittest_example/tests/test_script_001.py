from unittest import TestCase


class TestAddition(TestCase):
    def test_for_adding_numbers(self):
        assert (1 + 2 + 8 + 9) == 20

        with self.assertRaises(AssertionError):
            assert (0.1 + 0.2) == 0.3
