from unittest import TestCase
from unittest.mock import patch
from src.tgdownloader import TGDownloader
from telegram.client import Telegram, AuthorizationState

class Test_TGDownloader(TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def setUp(self) -> None:
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    @patch.object(Telegram, 'login', return_value=None)
    def test_loggin_in_returns_state(self, mock_login):
        # Arrange
        tgd = TGDownloader("API_ID", "API_HASH", "DB_ENC_KEY", "PHONE_NUMBER")
        
        # Act
        result = tgd.login()

        # Assert
        self.assertEqual(result, AuthorizationState.NONE)
        mock_login.assert_called_once()

    @patch.object(Telegram, 'stop', return_value=None)
    def test_stopping_succeeds(self, mock_stop):
        # Arrange
        tgd = TGDownloader("API_ID", "API_HASH", "DB_ENC_KEY", "PHONE_NUMBER")
        
        # Act
        tgd.stop()

        # Assert
        mock_stop.assert_called_once()

