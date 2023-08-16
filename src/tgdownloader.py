from telegram.client import Telegram

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