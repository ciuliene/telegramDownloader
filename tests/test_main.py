from io import TextIOWrapper
from unittest import TestCase
from unittest.mock import patch, mock_open, MagicMock
from src.menu import Menu

file_size = 20

class Mock_Chat:
    def __init__(self, title) -> None:
        self.title = title
        self.id = 0
        self.last_message_id = 0
        pass

class Mock_FileMessage:
    def __init__(self, file_name) -> None:
        self.file_name = file_name
        self.file_id = 0
        self.file_size = file_size
        self.telegram = None
        self.downloaded_size = 0
        self.is_downloaded = False
        self.file_path = None
        self.download_percentage = 0
        self.download_calls = 0
        pass

    def download(self) -> tuple[bool, int, str]:
        self.download_calls += 1
        self.downloaded_size += 1
        self.download_percentage = self.downloaded_size / self.file_size * 100
        if self.downloaded_size == self.file_size:
            self.is_downloaded = True
            self.file_path = "file_path"
        return self.is_downloaded, self.downloaded_size / self.file_size * 100, self.file_path # type: ignore


file_message_list = [Mock_FileMessage(
    "file_0"), Mock_FileMessage("file_1"), Mock_FileMessage("file_2"), Mock_FileMessage("file_3"), Mock_FileMessage("file_4")]

with patch('src.utils.print_progress_bar'):
    with patch('src.tgdownloader.TGDownloader') as mock_tgd:
        mock_tgd.return_value.get_chats.return_value = [Mock_Chat("chat_0"), Mock_Chat("chat_1")]
        mock_tgd.return_value.get_files_from_chat.return_value = file_message_list
        from main import run


class TestMain(TestCase):
    @patch.object(Menu, 'start_menu', return_value=("chat_0", 0))
    @patch('sys.stderr.write')
    @patch('builtins.open', new_callable=mock_open)
    def test_app_fails_when_generic_exception_is_raised(self, mock_file, mock_err_write, *_):
        # Arrange
        exception_message = "Test exception"
        mock_file.side_effect = [Exception(exception_message)]

        # Act
        run()

        # Assert
        self.assertEqual(1, mock_file.call_count)
        mock_file.assert_called_with("chat_0.txt", "r")
        mock_err_write.assert_called_once_with(
            f"\033[31m{exception_message}\033[0m")

    @patch.object(Menu, 'start_menu', return_value=("chat_0", 0))
    @patch('sys.stdout.write')
    @patch('sys.stderr.write')
    @patch('builtins.open', new_callable=mock_open)
    def test_app_returns_file_list_when_chat_file_does_not_exist(self, mock_file, mock_err_write, mock_out_write, *_):
        # Arrange
        mock_file_list = MagicMock()
        mock_file.side_effect = [FileNotFoundError, mock_file_list]

        # Act
        run()

        # Assert
        self.assertEqual(2, mock_file.call_count)
        mock_file.assert_called_with("chat_0.txt", "w")
        mock_err_write.assert_not_called()
        self.assertEqual(9 + len(file_message_list) * 2,
                         mock_out_write.call_count)
        mock_file_list.__enter__.assert_called_once()
        mock_file_list.__exit__.assert_called_once_with(None, None, None)
        self.assertEqual(len(file_message_list),
                         mock_file_list.__enter__.return_value.write.call_count)

    @patch.object(Menu, 'start_menu', return_value=("chat_0", 0))
    @patch('sys.stderr.write')
    @patch('builtins.open', new_callable=mock_open)
    def test_app_succeded_to_download_selected_files_from_chat(self, mock_file, mock_err_write, *_):
        # Arrange
        file_name = 'file_2'
        mock_file.return_value.__enter__.return_value.readlines.return_value = [
            "file_0\nfile_1\nfile_2", file_name]

        # Act
        run()

        # Assert
        self.assertEqual(1, mock_file.call_count)
        mock_file.assert_called_with("chat_0.txt", "r")
        mock_err_write.assert_not_called()
        for file in file_message_list:
            self.assertEqual(file_size if file.file_name ==
                             file_name else 0, file.download_calls)
