import sys
import unittest
from sys import platform


def setUpModule():
    pass


def tearDownModule():
    pass


class TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    @unittest.skip("This Feature Under Construction.")
    def test__function_feature_under_construction(self):
        with self.assertRaises(AssertionError):
            expected_result = 30
            assert expected_result == 1 + 2

    def test__skipping_this_test(self):
        self.skipTest("Errors Need to be pruned.")
        expected_result = 30
        assert expected_result == 10 + 20
        assert float("inf") == 1 / 0


@unittest.skip("Development in Progress")
class TestThisFrameworktestisSkipped(unittest.TestCase):
    @classmethod
    def test__this(cls):
        expected_result = 30
        assert expected_result == 1 + 3

    @classmethod
    def test__that(cls):
        expected_result = 30
        assert expected_result == 1 + 3


class TestDemo(unittest.TestCase):
    def test__that_run(self):
        self.assertEqual(1 + 1, 2)

    @unittest.skipIf(platform.startswith("win"), "Do not run on Windows")
    def test__that_does_not_run_on_windows(self):
        self.assertIsNotNone([])

    @unittest.skipUnless(sys.platform.startswith("win"), "reason")
    def test__for_windows_platform(self):
        self.assertEqual(1, 1, "anil")
