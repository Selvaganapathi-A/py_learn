import sys
import unittest
from sys import platform


def setUpModule():
    print("Running SetUp Module.")


def tearDownModule():
    print("Running Teardown Module.")


class Test_Case(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("Run Setup Class.")

    @classmethod
    def tearDownClass(cls) -> None:
        print("Run Teardown Class.")

    def setUp(self) -> None:
        print("Run Setup")
        return super(Test_Case, self).setUp()

    def tearDown(self) -> None:
        print("Run Teardown.")
        return super(Test_Case, self).tearDown()

    @unittest.skip("This Feature Under Construction.")
    def test_function_feature_under_construction(self):
        with self.assertRaises(AssertionError):
            assert 1 + 2 == 7

    def test_skipping_this_test(self):
        self.skipTest("Errors Need to be pruned.")
        assert 10 + 20 == 30
        assert 1 / 0 == float("inf")


@unittest.skip("Development in Progress")
class Test_This_Framework_test_is_Skipped(unittest.TestCase):

    def test_This(self):
        assert 1 + 3 == 4

    def test_That(self):
        assert 1 + 3 == 4


class TestDemo(unittest.TestCase):

    def test_that_run(self):
        self.assertEqual(1 + 1, 2)

    @unittest.skipIf(platform.startswith("win"), "Do not run on Windows")
    def test_that_does_not_run_on_windows(self):
        self.assertIsNotNone([])

    @unittest.skipUnless(sys.platform.startswith("win"), "reason")
    def test_for_windows_platform(self):
        self.assertEqual(1, 1, "anil")
