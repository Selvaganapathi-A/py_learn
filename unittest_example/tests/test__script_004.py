from unittest import TestCase


class TestBoolean(TestCase):
    def setUp(self):
        self.expected_result = 3
        return super().setUp()

    def test__true(self):
        self.assertTrue(self.expected_result == (1 + 2))

    def test__false(self):
        self.assertFalse(self.expected_result == (1 + 5))
