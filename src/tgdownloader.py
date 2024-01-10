from typing import Any
from telegram.client import Telegram
from src.models.chat import Chat
from src.models.file_message import FileMessage
import os

class TGDownloader():
    def __init__(self, api_id: str, api_hash:str, database_encryption_key:str, phone:str, files_directory: str = None) -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.database_encryption_key = database_encryption_key
        self.phone = phone

        if files_directory is not None:
            self._check_directory(files_directory)

        self.tg = Telegram(
            api_id=api_id,
            api_hash=api_hash,
            phone=phone,
            database_encryption_key=database_encryption_key,
            files_directory=files_directory,
            tdlib_verbosity=0
        )
        pass

    def login(self):
        self.tg.login()
        return self.tg.authorization_state
    
    def stop(self):
        self.tg.stop()

    def get_chats(self) -> list[Chat]:
        result = self.tg.get_chats()
        result.wait()
        
        chats = []

        for chat_id in result.update['chat_ids']:
            result = self.tg.get_chat(chat_id)
            result.wait()
            chat = result.update
            chats.append(Chat(title=chat['title'], id=chat['id'], last_message_id=chat['last_message']['id']))

        return chats

    def _get_chat_history(self, chat_id: int, limit: int = 100, from_message_id: int = 0) -> list[dict]:
        result = self.tg.get_chat_history(chat_id, limit=limit, from_message_id=from_message_id)
        result.wait()
        return result.update['messages']

    def _get_latest_n_files_from_chat(self, chat_id: int, limit: int = 100, from_message_id: int = 0) -> list[FileMessage]:
        messages = self._get_chat_history(chat_id, limit=limit, from_message_id=from_message_id)
        video_list = []

        for message in messages:
            field = 'video' if 'video' in message['content'] else 'document' if 'document' in message[
                'content'] else 'web_page' if 'web_page' in message['content'] else None

            if not field:
                continue

            video = message['content'][field]

            if field == 'web_page':
                if not 'document' in video:
                    continue
                file_name = video['document']['file_name']
                file_id = video['document']['document']['id']
                file_size = video['document']['document']['size']
            else:
                file_name = video['file_name']
                file_id = video[field]['id']
                file_size = video[field]['size']

            video_list.append(FileMessage(
                file_name=file_name,
                file_id=file_id,
                file_size=file_size,
                telegram=self.tg,
                id=message['id']))

        return video_list

    def get_files_from_chat(self, chat: Chat) -> list[FileMessage]:
        file_list = []
        last_message_id = chat.last_message_id

        while True:
            files = self._get_latest_n_files_from_chat(
                chat.id, from_message_id=last_message_id)

            if len(files) == 0:
                break

            for file in files:
                file_list.append(file)

            last_message_id = file_list[-1].id

        return sorted(file_list, key=lambda file: file.id)

    def __call__(self, *args: Any, **kwds: Any) -> Telegram:
        return self.tg
    
    def _check_directory(self, directory: str):
        if not os.path.exists(directory):
            os.makedirs(directory)