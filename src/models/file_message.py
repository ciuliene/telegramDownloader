class FileMessage():
    def __init__(self, file_name: str, file_id: int, file_size: int) -> None:
        self.file_name = file_name
        self.file_id = file_id
        self.file_size = file_size
        pass

    def __repr__(self) -> str:
        return self.file_name