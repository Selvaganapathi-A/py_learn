from unittest import TestCase


class Test_Boolean(TestCase):
    def test_true(self):
        self.assertTrue(((1 + 2) == 3) is True)

    def test_false(self):
        self.assertFalse(((1 + 5) == 3))
