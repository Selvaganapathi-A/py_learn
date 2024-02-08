from unittest import TestCase


class Test_String(TestCase):

    def test_add(self):
        assert "Hi! " + "John" == "Hi! John"

    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")

    def test_is_upper(self):
        self.assertTrue("FOO".isupper())
        self.assertFalse("Foo".isupper())

    def test_lower(self):
        self.assertEqual("lili".lower(), "lili")

    def test_is_lower(self):
        self.assertTrue("lili".islower())
        self.assertFalse("Lily".islower())

    def test_split(self):
        s = "hello world"
        self.assertEqual(s.split(), ["hello", "world"])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(" ", 2)
            raise TypeError
