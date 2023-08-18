from unittest import TestCase
from unittest.mock import patch
from src.menu import Menu

file_size = 10

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
        pass

    def download(self) -> tuple[bool, int, str]:
        self.downloaded_size += 1
        self.download_percentage = self.downloaded_size / self.file_size * 100
        if self.downloaded_size == self.file_size:
            self.is_downloaded = True
            self.file_path = "file_path"
        return self.is_downloaded, self.downloaded_size / self.file_size * 100, self.file_path

with patch('src.envtool.EnvTool'):
        with patch('src.utils.print_progress_bar'):
            with patch('src.tgdownloader.TGDownloader') as mock_tgd:
                mock_tgd.return_value.get_chats.return_value = [Mock_Chat("chat_0"), Mock_Chat("chat_1")]
                mock_tgd.return_value.get_files_from_chat.return_value = [Mock_FileMessage("file_0"), Mock_FileMessage("file_1"), Mock_FileMessage("file_1"), Mock_FileMessage("file_1")]
                from main import run


class TestMain(TestCase):
    @patch.object(Menu, 'start_menu', return_value=("chat_0", 0))
    @patch('sys.stderr.write')
    @patch('sys.stdout.write')
    def test_running_app_calls_stdout_write_n_times_for_each_progress(self, mock_out_write, mock_err_write, *_):
        # Act
        run()

        # Assert
        self.assertEqual(file_size + 4, mock_out_write.call_count)
        mock_err_write.assert_not_called()

    @patch.object(Menu, 'start_menu', side_effect=KeyboardInterrupt())
    @patch('sys.stderr.write')
    @patch('sys.stdout.write')
    def test_running_app_ends_on_user_interruption(self, mock_out_write, mock_err_write, *_):
        # Act
        run()

        # Assert
        mock_out_write.assert_called_once_with("\033[?25h")
        mock_err_write.assert_not_called()

    @patch.object(Menu, 'start_menu', side_effect=Exception("Mocked exception"))
    @patch('sys.stderr.write')
    @patch('sys.stdout.write')
    def test_running_app_ends_on_exception(self, mock_out_write, mock_err_write, *_):
        # Act
        run()

        # Assert
        mock_out_write.assert_called_once_with("\033[?25h")
        mock_err_write.assert_called_once_with("\x1b[31mMocked exception\x1b[0m")

