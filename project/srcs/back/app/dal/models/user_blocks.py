from datetime import datetime

class UserBlocks:
    def __init__(
        self,
        blocker_id: int,
        blocked_id: int,
        created_at: datetime = None,
        create : bool = True
    ) :        
        if not create:
            self.created_at = created_at
        self.blocker_id = blocker_id
        self.blocked_id = blocked_id
