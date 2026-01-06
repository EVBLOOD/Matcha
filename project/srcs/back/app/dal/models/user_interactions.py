class UserInteractions:
    def __init__(
        self,
        liker_id: int,
        liked_id: int,
        status: str,
        id: int = None,
        create : bool = True
    ) :
        print(f"xyz -", flush=True)
        
        if not create:
            self.id = id
        else :
            self.id = None
        print(f"xyz -", flush=True)

        self.liker_id = liker_id
        self.liked_id = liked_id
        self.status = status
        print(f"xyz", flush=True)
