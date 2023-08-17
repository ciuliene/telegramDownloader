class Chat():
    def __init__(self, title: str, id: str) -> None:
        self.title = title
        self.id = id
        pass
    
    def __repr__(self) -> str:
        return f'{self.title} ({self.id})'