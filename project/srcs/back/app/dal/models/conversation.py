class Conversation:
    def __init__(
        self,
        user1_id: int,
        user2_id: str,
        id: int = None
    ) :
        self.id = id
        self.user1_id = user1_id
        self.user2_id = user2_id
