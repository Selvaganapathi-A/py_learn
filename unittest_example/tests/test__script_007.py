from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from py_learn.unittest_example import fileio


class Test001(TestCase):
    def test__sum_numbers(self):
        fileio.read_numbers_from_file = Mock()
        fileio.read_numbers_from_file.return_value = [
            900,
            800,
            1200,
            1100,
        ]
        self.assertEqual(
            fileio.sum_of_numbers(Path(__file__).parent / 'dumme.input'),
            4000,
        )


class Test002(TestCase):
    def test__sum_numbers(self):
        fileio.read_numbers_from_file = MagicMock()
        fileio.read_numbers_from_file.return_value = [
            900,
            800,
            1200,
            1100,
        ]
        self.assertEqual(
            fileio.sum_of_numbers(Path(__file__).parent / 'dumme.input'),
            4000,
        )


class Test003(TestCase):
    @patch('py_learn.unittest_example.fileio.read_numbers_from_file')
    def test__sum_numbers(self, mock_function: Mock):
        mock_function.return_value = [900, 800, 1200, 1100]
        self.assertEqual(
            fileio.sum_of_numbers(Path(__file__).parent / 'dumme.input'),
            4000,
        )


class Test004(TestCase):
    def test__sum_numbers(self):
        with patch('py_learn.unittest_example.fileio.read_numbers_from_file') as mock_function:
            mock_function.return_value = [900, 800, 1200, 1100]
            self.assertEqual(
                fileio.sum_of_numbers(Path(__file__).parent / 'dumme.input'),
                4000,
            )


class Test005(TestCase):
    def test__sum_numbers(self):
        patcher = patch('py_learn.unittest_example.fileio.read_numbers_from_file')
        mock_function = patcher.start()
        mock_function.return_value = [900, 800, 1200, 1100]
        self.assertEqual(
            fileio.sum_of_numbers(Path(__file__).parent / 'dumme.input'),
            4000,
        )
        patcher.stop()
