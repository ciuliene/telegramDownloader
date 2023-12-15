from unittest import TestCase
from unittest.mock import patch, call
from src.rename import *


class TestRename(TestCase):
    @patch('os.rename')
    def test_renaming_with_index_called_with_expected_parameters(self, mock_rename):
        # Arrange
        path_to = 'path/to/'
        files = ['file1', 'file2', 'file3']
        ordered_list = [f'{path_to}{files[0]}',
                        f'{path_to}{files[1]}', f'{path_to}{files[2]}']
        expected_calls = [call(ordered_list[0], f'{path_to}001_{files[0]}'),
                          call(ordered_list[1], f'{path_to}002_{files[1]}'),
                          call(ordered_list[2], f'{path_to}003_{files[2]}')]

        # Act
        rename_with_index(ordered_list)

        # Assert
        mock_rename.assert_has_calls(expected_calls)

    @patch('os.rename')
    def test_renaming_with_index_called_with_custom_padding(self, mock_rename):
        # Arrange
        path_to = 'path/to/'
        files = ['file1', 'file2', 'file3']
        ordered_list = [f'{path_to}{files[0]}',
                        f'{path_to}{files[1]}', f'{path_to}{files[2]}']
        expected_calls = [call(ordered_list[0], f'{path_to}0001_{files[0]}'),
                          call(ordered_list[1], f'{path_to}0002_{files[1]}'),
                          call(ordered_list[2], f'{path_to}0003_{files[2]}')]

        # Act
        rename_with_index(ordered_list, 4)

        # Assert
        mock_rename.assert_has_calls(expected_calls)

    @patch('os.path.isfile', return_value=True)
    @patch('os.listdir')
    @patch('os.rename')
    def test_removing_index_from_file_names_called_with_expected_parameters(self, mock_rename, mock_listdir, *_):
        # Arrange
        path_to = 'path/to/'
        files = ['001_file1', '002_file2', '003_file3']
        mock_listdir.return_value = files
        expected_calls = [call(f'{path_to}{files[0]}', f'{path_to}file1'),
                          call(f'{path_to}{files[1]}', f'{path_to}file2'),
                          call(f'{path_to}{files[2]}', f'{path_to}file3')]

        # Act
        remove_index(path_to)

        # Assert
        mock_rename.assert_has_calls(expected_calls)
