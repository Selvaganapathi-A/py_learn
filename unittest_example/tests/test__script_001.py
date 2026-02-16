from unittest import TestCase


class TestAddition(TestCase):
    def test__for_adding_numbers(self):
        total = 20
        assert total == (1 + 2 + 8 + 9)
        with self.assertRaises(AssertionError):
            total = 0.3
            assert total == (0.1 + 0.2)
