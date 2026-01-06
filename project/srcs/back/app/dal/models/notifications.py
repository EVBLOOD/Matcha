from datetime import datetime

class Notification:
    def __init__(
        self,
        id: int = None,
        user_id: int = None,
        type: str = None,
        source_user_id: int = None,
        is_read: bool = None,
        created_at: datetime = None,
        insertion_check: bool = True
    ):
        
        if insertion_check \
              and not self.isvalid_type(type) :
            raise ValueError
        self.id = id
        self.user_id = user_id
        self.type = type
        self.source_user_id = source_user_id
        self.is_read = is_read
        self.created_at = created_at

    def isvalid_type(self, type: str) :
        return type in ['like', 'view', 'message', 'match', 'unmatch']

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type,
            "source_user_id": self.source_user_id,
            "is_read": self.is_read,
            "created_at": self.created_at,
            "is_verified": self.is_verified
        } 