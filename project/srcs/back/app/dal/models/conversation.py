class Conversation:
    def __init__(
        self,
        user1_id: int,
        user2_id: str,
        created_at = None,
        id: int = None,
    ) :
        self.id = id
        self.created_at = created_at
        self.user1_id = user1_id
        self.user2_id = user2_id


# matcha_back  | (27, 50, 1, datetime.datetime(2026, 1, 8, 11, 12, 30, 809812, tzinfo=datetime.timezone.utc))

