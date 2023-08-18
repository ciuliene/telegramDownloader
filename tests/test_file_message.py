from unittest import TestCase
from unittest.mock import patch, MagicMock
from src.models.file_message import FileMessage

class MockResult:
    def __init__(self, update: dict) -> None:
        self.update = update

    def wait(self):
        pass

class TestFileMessage(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def setUp(self) -> None:
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def get_telegram_mock(self, download_complete: bool = False, percentage: int = 0):
        telegram = MagicMock()
        telegram.add_update_handler = MagicMock(return_value=None)
        telegram.call_method.return_value = MockResult({'local': {'is_downloading_completed': download_complete, 'downloaded_size': percentage, 'path': 'test_path'}})
        return telegram

    def test_downloading_file_returns_false_when_downloading_is_not_completed(self):
        # Arrange
        telegram = self.get_telegram_mock()
        file = FileMessage(file_name='test_file', file_id=1, file_size=100, telegram=telegram)

        # Act
        result, percentage, path = file.download()

        # Assert
        self.assertFalse(result)
        self.assertEqual(percentage, 0)
        self.assertIsNone(path)

    def test_downloading_file_returns_true_when_downloading_is_completed(self):
        # Arrange
        telegram = self.get_telegram_mock(True, 100)
        file = FileMessage(file_name='test_file', file_id=1, file_size=100, telegram=telegram)

        # Act
        result, percentage, path = file.download()

        # Assert
        self.assertTrue(result)
        self.assertEqual(percentage, 100)
        self.assertEqual(path, 'test_path')
