class Message:
    def __init__(
        self,
        id: int,
        conversation_id: int,
        sender_id: int,
        content: str,
        is_read: bool
    ) :
        self.id = id
        self.conversation_id = conversation_id
        self.sender_id = sender_id
        self.content = content
        self.is_read = is_read
