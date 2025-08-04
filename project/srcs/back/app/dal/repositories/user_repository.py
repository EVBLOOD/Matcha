from app.dal.base_repository import BaseRepository
from app.dal.models.user import User
from typing import Optional
import secrets

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
        token_verify  = cls.create_verify_token(user_id=user_id)
        print (token_verify, flush=True)
        # if user_id is not None :
        #     cls.send_email(user_data.email, user_data.username, token_verify)
        return user_id
    
    @classmethod
    def create_verify_token(cls, user_id: int) :
        trying = 0
        query = """
            UPDATE users 
            SET verification_token = %s 
            WHERE id = %s
            RETURNING id
        """
        while trying < 15 :
            try :
                verification_token = secrets.token_urlsafe(32)
                cls._execute(query, (verification_token, user_id))
                return verification_token
            except Exception as e :
                trying += 1
        return None
    
    
    @classmethod
    def find_by_verification_token(cls, token: str) :
        query = "SELECT id, is_verified FROM users WHERE verification_token = %s"
        user_infos = cls._fetch_one(query, (token))
        return user_infos.id, user_infos.is_verified

    @classmethod
    def verify_token(cls, user_id: int):
        query = """
            UPDATE users 
            SET is_verified = TRUE
            WHERE id = %s
        """
        cls._execute(query, (user_id,))

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
