from app.dal.base_repository import BaseRepository
from app.dal.models.user import User
from typing import Optional

class UserRepository(BaseRepository):
    _table_name = "users"
    _columns = [
        "id", "username", "first_name", "last_name", 
        "password_hash", "email", "fame_rating",
        "latitude", "longitude", "is_verified"
    ]

    _columns_insertion = [
        "username", "first_name", "last_name", 
        "password_hash", "email"
    ]

    @classmethod
    def create_user(cls, user_data: User) -> Optional[User]:
        norm_data = {
            'username' : user_data.username,
            'first_name' : user_data.first_name,
            'last_name' : user_data.last_name,
            'password_hash' : user_data.password_hash,
            'email' : user_data.email
        }
        user_id = cls.insert(table_name=cls._table_name, columns=cls._columns_insertion, data=norm_data)
        return user_id

    @classmethod
    def find_by_email(cls, email: str) -> Optional[User]:
        query = "SELECT * FROM users WHERE email = %s"
        row = cls._fetch_one(query, (email,))
        return User(*row) if row else None

    @classmethod
    def find_by_username(cls, username: str) -> Optional[User]:
        query = "SELECT * FROM users WHERE username = %s"
        row = cls._fetch_one(query, (username,))
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