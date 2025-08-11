class UserInteractions:
    def __init__(
        self,
        id: int,
        liker_id: int,
        liked_id: int,
        status: str,
        create : bool = True
    ) :
        if create:
            self.id = id
        else :
            self.id = None
        self.liker_id = liker_id
        self.liked_id = liked_id
        self.status = status
