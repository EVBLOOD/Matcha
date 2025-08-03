from data_access_layer.base_repository import BaseRepository
from data_access_layer.models.user import User
from typing import Optional

class UserRepository(BaseRepository):
    _table_name = "users"
    _columns = [
        "id", "username", "first_name", "last_name", 
        "password_hash", "email", "fame_rating",
        "latitude", "longitude", "is_verified"
    ]

    @classmethod
    def create_user(cls, user_data: dict) -> Optional[User]:
        user_id = cls.insert(user_data)
        return cls.find_by_id(user_id)

    @classmethod
    def find_by_email(cls, email: str) -> Optional[User]:
        query = "SELECT * FROM users WHERE email = %s"
        row = cls._fetch_one(query, (email,))
        return User(*row) if row else None

    @classmethod
    def update_last_online(cls, user_id: int):
        query = """
            UPDATE users 
            SET last_online = CURRENT_TIMESTAMP 
            WHERE id = %s
        """
        cls._execute(query, (user_id,))

    @classmethod
    def update_location(
        cls, 
        user_id: int, 
        latitude: float, 
        longitude: float
    ) -> bool:
        query = """
            UPDATE users 
            SET latitude = %s, longitude = %s 
            WHERE id = %s
        """
        return cls._execute(query, (latitude, longitude, user_id)) > 0