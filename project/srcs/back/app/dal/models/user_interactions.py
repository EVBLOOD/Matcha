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


# CREATE TABLE user_interactions (
#     id SERIAL PRIMARY KEY,
#     liker_id INT REFERENCES users(id) ON DELETE CASCADE,
#     liked_id INT REFERENCES users(id) ON DELETE CASCADE,
#     status VARCHAR(10) NOT NULL CHECK (status IN ('liked', 'disliked')),
#     created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
#     UNIQUE (liker_id, liked_id)
# );

