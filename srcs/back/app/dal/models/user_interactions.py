class UserInteractions:
    def __init__(
        self,
        liker_id: int,
        liked_id: int,
        status: str,
        id: int = None,
        create : bool = True
    ) :        
        if not create:
            self.id = id
        else :
            self.id = None
        self.liker_id = liker_id
        self.liked_id = liked_id
        self.status = status
