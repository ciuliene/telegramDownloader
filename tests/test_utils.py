from unittest import TestCase
from io import StringIO
import sys
from src.utils import *

class TestPrintProgressBar(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def setUp(self):
        self.saved_stdout = sys.stdout
        self.mock_stdout = StringIO()
        sys.stdout = self.mock_stdout

    def tearDown(self):
        sys.stdout = self.saved_stdout
        sys.stdout.write("\033[?25h")

    def test_creating_progress_bar_prints_expected_string(self):
        # Arrange
        file_name = "example_file.txt"
        percentage = 80.0
        name_size = 15
        bar_size = 60
        expected_output = f'\x1b[?25l\x1b[K example_file.tx\t[\x1b[42m{" " * int(bar_size * ((percentage) / 100))}\x1b[0m{"-" * int(bar_size * ((100-percentage) / 100))}] {percentage:.2f}%\n'

        # Act
        print_progress_bar(file_name, percentage, name_size)
        actual_output = self.mock_stdout.getvalue()

        # Assert
        self.assertEqual(expected_output, actual_output)

    def test_creating_progress_bar_with_custom_length_prints_expected_string(self):
        # Arrange
        file_name = "example_file.txt"
        percentage = 25.0
        name_size = 15
        bar_size = 20
        expected_output = f'\x1b[?25l\x1b[K example_file.tx\t[\x1b[42m{" " * int(bar_size * ((percentage) / 100))}\x1b[0m{"-" * int(bar_size * ((100-percentage) / 100))}] {percentage:.2f}%\n'

        # Act
        print_progress_bar(file_name, percentage, name_size, bar_size)
        actual_output = self.mock_stdout.getvalue()

        # Assert
        self.assertEqual(expected_output, actual_output)

    def test_invalid_percentage_raises_value_error(self):
        # Act
        with self.assertRaises(ValueError):
            print_progress_bar("example_file.txt", 110, 15)
