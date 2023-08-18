from telegram.client import Telegram

class FileMessage():
    def __init__(self, file_name: str, file_id: int, file_size: int, telegram: Telegram) -> None:
        self.file_name = file_name
        self.file_id = file_id
        self.file_size = file_size
        self.telegram = telegram
        self.downloaded_size = 0
        self.is_downloaded = False
        self.file_path = None
        pass

    def download(self) -> tuple[bool, int, str]:
        result = self.telegram.call_method('downloadFile', params={'file_id': self.file_id, 'priority': 1})
        result.wait()
        self.downloaded_size = result.update['local']['downloaded_size']
        if self.downloaded_size == self.file_size:
            self.is_downloaded = True
            self.file_path = result.update['local']['path']

        return self.is_downloaded, self.downloaded_size / self.file_size * 100, self.file_path

    def __repr__(self) -> str:
        return self.file_name
