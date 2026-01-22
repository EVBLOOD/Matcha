

class Picture:
    def __init__(
        self,
        id: int,
        user_id: int,
        url: str,
        is_profile_picture: bool,
        created_at = None
    ) :
        self.id = id
        self.user_id = user_id
        self.url = url
        self.is_profile_picture = is_profile_picture
        self.created_at = created_at
