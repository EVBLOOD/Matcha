from app.dal.base_repository import BaseRepository
from app.dal.models.user_interactions import UserInteractions

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
        query = """
        SELECT
            liked_id,
            u.username,
            u.first_name,
            u.last_name,
            (
                SELECT json_agg(json_build_object('url', up.url, 'is_profile_picture', up.is_profile_picture))
                FROM user_pictures up
                WHERE up.user_id = liked_id AND up.is_profile_picture = TRUE
            ) AS profile_picture_url
        FROM user_interactions 
        LEFT JOIN profiles p ON liked_id = p.user_id
        LEFT JOIN users u ON liked_id = u.id
        WHERE liker_id = %s
        """
        rows = cls._fetch_all(query, (user_id,))
        return rows

    @classmethod
    def get_user_likers_list(cls, user_id: str) :
        query = """
        SELECT
            liker_id,
            u.username,
            u.first_name,
            u.last_name,
            (
                SELECT json_agg(json_build_object('url', up.url, 'is_profile_picture', up.is_profile_picture))
                FROM user_pictures up
                WHERE up.user_id = liker_id AND up.is_profile_picture = TRUE
            ) AS profile_picture_url,
            (SELECT COUNT(*) FROM user_interactions WHERE liked_id = u.id AND liker_id = %s) as liked_back
        FROM user_interactions 
        LEFT JOIN profiles p ON liker_id = p.user_id
        LEFT JOIN users u ON liker_id = u.id
        WHERE liked_id = %s
        """
        rows = cls._fetch_all(query, (user_id, user_id))
        return rows
    
    @classmethod
    def get_user_interaction_existance(cls, liker_id: str, liked_id: str) :
        query = "SELECT id FROM user_interactions WHERE liker_id = %s AND liked_id = %s"
        row = cls._fetch_one(query, (liker_id, liked_id,))
        return row
    
    @classmethod
    def are_users_connected(cls, liker_id: str, liked_id: str) :
        query = "SELECT id FROM user_interactions WHERE (liker_id = %s AND liked_id = %s) OR (liker_id = %s AND liked_id = %s)"
        row = cls._fetch_all(query, (liker_id, liked_id,liked_id ,liker_id,))
        return len(row) == 2

    @classmethod
    def remove_user_interaction_existance(cls, liker_id: str, liked_id: str) :
        id = cls.get_user_interaction_existance(liker_id, liked_id)
        if not id :
            return None
        return cls.delete(id)
