class Chat():
    def __init__(self, title: str, id: str, last_message_id: str) -> None:
        self.title = title
        self.id = id
        self.last_message_id = last_message_id
        pass
    
    def __repr__(self) -> str:
        return f'{self.title} ({self.id})'