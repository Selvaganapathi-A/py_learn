from unittest import TestCase


class TestString(TestCase):
    @staticmethod
    def test__add():
        assert 'Hi! ' + 'John' == 'Hi! John'

    def test__upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test__is_upper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test__lower(self):
        self.assertEqual('lili'.lower(), 'lili')

    def test__is_lower(self):
        self.assertTrue('lili'.islower())
        self.assertFalse('Lily'.islower())

    def test__split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(' ', 2)
            raise TypeError
