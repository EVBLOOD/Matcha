from app.dal.base_repository import BaseRepository
from app.dal.models.user_interactions import UserInteractions
# CREATE TABLE user_interactions (
#     id SERIAL PRIMARY KEY,
#     liker_id INT REFERENCES users(id) ON DELETE CASCADE,
#     liked_id INT REFERENCES users(id) ON DELETE CASCADE,
#     status VARCHAR(10) NOT NULL CHECK (status IN ('liked', 'disliked')),
#     created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
#     UNIQUE (liker_id, liked_id)
# );


class UserInteractionsRepository(BaseRepository):
    _table_name = "user_interactions"
    _columns = [
        "id", "liker_id", "liked_id", "status"
    ]
    _insert_columns = [
        "liker_id", "liked_id", "status"
    ]
    @classmethod
    def create_user_interactions(cls, user_interaction: UserInteractions) :
        norm_data = {
            'liker_id' : user_interaction.liker_id,
            'liked_id' : user_interaction.liked_id,
            'status' : user_interaction.status
        }

        id = cls.insert(table_name=cls._table_name, columns=cls._insert_columns, data=norm_data, returning="id")
        return id

    @classmethod
    def get_user_liked_list(cls, user_id: str) :
        query = "SELECT liked_id FROM user_interactions WHERE liker_id = %s"
        rows = cls._fetch(query, (user_id,))
        return rows

    @classmethod
    def get_user_likers_list(cls, user_id: str) :
        query = "SELECT liker_id FROM user_interactions WHERE liked_id = %s"
        rows = cls._fetch(query, (user_id,))
        return rows
    
    @classmethod
    def get_user_interaction_existance(cls, liker_id: str, liked_id: str) :
        query = "SELECT id FROM user_interactions WHERE liker_id = %s AND liked_id = %s"
        row = cls._fetch_one(query, (liker_id, liked_id,))
        return (row is not None)
    
        