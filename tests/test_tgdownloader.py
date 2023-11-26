from unittest import TestCase
from unittest.mock import patch
from telegram.client import Telegram, AuthorizationState
from src.tgdownloader import TGDownloader

class Mock_Chats():
    def __init__(self, len = 0) -> None:
        chats = []
        for i in range(len):    
            chats.append({'title': f'Chat {i}', 'id': str(i)})
        self.update = {'chat_ids': chats}
        pass

    def wait(self):
        pass

class Mock_Chat():
    id = 0
    last_message_id = 0
    def __init__(self, id: 0) -> None:
        self.update = {'title': f'Chat {id}', 'id': str(id), 'last_message': {'id': str(id)}}
        self.id = id
        self.last_message_id = id
        pass

    def wait(self):
        pass

class Mock_History():
    def __init__(self, len: int = 0, msg_type: str = 'video') -> None:
        messages = []
        for i in range(len):
            messages.append({'id': str(i), 'content': {msg_type: {'file_name': f'video_{i}.mp4', msg_type:{'id':i, 'size':i}  }}})
        self.update = {'messages': messages}
        pass

    def wait(self):
        pass

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
        self.assertIsInstance(tgd(), Telegram)

    @patch.object(Telegram, 'stop', return_value=None)
    def test_stopping_succeeds(self, mock_stop):
        # Arrange
        tgd = TGDownloader("API_ID", "API_HASH", "DB_ENC_KEY", "PHONE_NUMBER")
        
        # Act
        tgd.stop()

        # Assert
        mock_stop.assert_called_once()

    @patch.object(Telegram, 'stop', return_value=None)
    @patch('os.makedirs')
    def test_creating_directory_succeeds(self, mock_makedirs, _):
        # Arrange
        TGDownloader("API_ID", "API_HASH", "DB_ENC_KEY", "PHONE_NUMBER", "test_directory")

        # Assert
        mock_makedirs.assert_called_once()

    @patch.object(Telegram, 'get_chat')
    @patch.object(Telegram, 'get_chats')
    def test_getting_chats_returns_empty_chat_list(self, mock_chats, mock_chat):
        # Arrange
        tgd = TGDownloader("API_ID", "API_HASH", "DB_ENC_KEY", "PHONE_NUMBER")
        mock_chats.return_value = Mock_Chats(1)
        mock_chat.return_value = Mock_Chat(0)

        # Act
        result = tgd.get_chats()

        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual('Chat 0 (0)', str(result[0]))

    @patch.object(Telegram, 'get_chat_history')
    def test_getting_files_returns_empty_list(self, mock_history):
        # Arrange
        tgd = TGDownloader("API_ID", "API_HASH", "DB_ENC_KEY", "PHONE_NUMBER")
        mock_history.return_value = Mock_History()
        chat = Mock_Chat(0)

        # Act
        result = tgd.get_files_from_chat(chat)

        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    @patch.object(Telegram, 'get_chat_history')
    def test_getting_files_returns_one_message(self, mock_history):
        # Arrange
        tgd = TGDownloader("API_ID", "API_HASH", "DB_ENC_KEY", "PHONE_NUMBER")
        mock_history.side_effect = [Mock_History(1), Mock_History()]
        chat = Mock_Chat(0)

        # Act
        result = tgd.get_files_from_chat(chat)

        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual('video_0.mp4', str(result[0]))

    @patch.object(Telegram, 'get_chat_history')
    def test_getting_files_returns_empty_list_when_message_is_not_video_type(self, mock_history):
        # Arrange
        tgd = TGDownloader("API_ID", "API_HASH", "DB_ENC_KEY", "PHONE_NUMBER")
        mock_history.side_effect = [Mock_History(1, 'image'), Mock_History()]
        chat = Mock_Chat(0)

        # Act
        result = tgd.get_files_from_chat(chat)

        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    @patch.object(Telegram, 'get_chat_history')
    def test_getting_files_returns_list_when_chat_has_multiple_files(self, mock_history):
        # Arrange
        tgd = TGDownloader("API_ID", "API_HASH", "DB_ENC_KEY", "PHONE_NUMBER")
        mock_history.side_effect = [Mock_History(
            10), Mock_History(5), Mock_History()]
        chat = Mock_Chat(0)

        # Act
        result = tgd.get_files_from_chat(chat)

        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 15)
