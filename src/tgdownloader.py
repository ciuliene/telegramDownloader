from typing import Any
from telegram.client import Telegram
from src.models.chat import Chat

class TGDownloader():
    def __init__(self, api_id: str, api_hash:str, database_encryption_key:str, phone:str) -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.database_encryption_key = database_encryption_key
        self.phone = phone

        self.tg = Telegram(
            api_id=api_id,
            api_hash=api_hash,
            phone=phone,
            database_encryption_key=database_encryption_key,
        )
        pass

    def login(self):
        self.tg.login()
        return self.tg.authorization_state
    
    def stop(self):
        self.tg.stop()

    def get_chats(self) -> list:
        result = self.tg.get_chats()
        result.wait()
        
        chats = []

        for chat_id in result.update['chat_ids']:
            result = self.tg.get_chat(chat_id)
            result.wait()
            chat = result.update
            chats.append(Chat(title=chat['title'], id=chat['id']))

        return chats

    def __call__(self, *args: Any, **kwds: Any) -> Telegram:
        return self.tg
        