from unittest import TestCase
from unittest.mock import patch, mock_open
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

    def test_going_back_n_lines_prints_expected_string(self):
        # Arrange
        n = 5
        expected_output = "\033[F".join(["" for _ in range(n)] + [""])

        # Act
        go_back_n_lines(n)
        actual_output = self.mock_stdout.getvalue()

        # Assert
        self.assertEqual(expected_output, actual_output)

    def test_going_back_zero_lines_prints_expected_string(self):
        # Arrange
        n = 0
        expected_output = "\033[F".join(["" for _ in range(n)] + [""])

        # Act
        go_back_n_lines(n)
        actual_output = self.mock_stdout.getvalue()

        # Assert
        self.assertEqual(expected_output, actual_output)

    def test_going_forward_n_lines_prints_expected_string(self):
        # Arrange
        n = 5
        expected_output = "\033[E".join(["" for _ in range(n)] + [""])

        # Act
        go_forward_n_lines(n)
        actual_output = self.mock_stdout.getvalue()

        # Assert
        self.assertEqual(expected_output, actual_output)
    
    def test_going_forward_zero_lines_prints_expected_string(self):
        # Arrange
        n = 0
        expected_output = "\033[E".join(["" for _ in range(n)] + [""])

        # Act
        go_forward_n_lines(n)
        actual_output = self.mock_stdout.getvalue()

        # Assert
        self.assertEqual(expected_output, actual_output)

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

    def test_getting_file_list_from_file_raise_not_found_exception_when_file_does_not_exits(self):
        # Act
        with self.assertRaises(FileNotFoundError):
            get_file_list_from_file("not_existing_file.txt")

    @patch('builtins.open', new_callable=mock_open, read_data="")
    def test_getting_file_list_from_file_returns_empty_list(self, *_):
        # Arrange
        expected_output = []

        # Act
        actual_output = get_file_list_from_file("tests/test_files.txt")

        # Assert
        self.assertEqual(expected_output, actual_output)

    @patch('builtins.open', new_callable=mock_open, read_data="file_0\nfile_1\nfile_2")
    def test_getting_file_list_from_file_returns_expected_list(self, *_):
        # Arrange
        expected_output = ["file_0", "file_1", "file_2"]

        # Act
        actual_output = get_file_list_from_file("tests/test_files.txt")

        # Assert
        self.assertEqual(expected_output, actual_output)

    @patch('builtins.open', new_callable=mock_open)
    def test_writing_file_list_return_success_when_list_is_empty(self, mock_open):
        # Arrange
        file_name = "tests/test_files.txt"
        file_list = []

        # Act
        store_files_file_in_file(file_name, file_list)

        # Assert
        self.assertEqual(3 + len(file_list), len(mock_open.mock_calls))

    @patch('builtins.open', new_callable=mock_open)
    def test_writing_file_list_return_success_when_list_is_not_empty(self, mock_open):
        # Arrange
        file_name = "tests/test_files.txt"
        file_list = ["file_0", "file_1", "file_2"]

        # Act
        store_files_file_in_file(file_name, file_list)

        # Assert
        self.assertEqual(3 + len(file_list), len(mock_open.mock_calls))
