from app.dal.base_repository import BaseRepository
from app.dal.models.user import User
from typing import Optional
import secrets

import re
import random
import string

class UserRepository(BaseRepository):
    _table_name = "users"
    _columns = [
        "id", "username", "first_name", "last_name", 
        "password_hash", "email", "fame_rating",
        "latitude", "longitude", "is_verified", "birthdate"
    ]
    _columns_insertion = [
        "username", "first_name", "last_name", 
        "password_hash", "email", "birthdate"
    ]

    _columns_insertion_oauth = [
        "username", "first_name", "last_name", "email", "is_verified"#, "birthdate"
    ]

    @classmethod
    def create_user(cls, user_data: User) -> Optional[User]:
        norm_data = {
            'username' : user_data.username,
            'first_name' : user_data.first_name,
            'last_name' : user_data.last_name,
            'password_hash' : user_data.password_hash,
            'email' : user_data.email,
            'birthdate' : user_data.birthdate
        }
        user_id = cls.insert(table_name=cls._table_name, columns=cls._columns_insertion, data=norm_data)
        token_verify  = cls.create_verify_token(user_id=user_id)

        return user_data, token_verify, user_id
    
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
        value = cls._fetch_one(query, (token, ))
        user_infos_id, user_infos_is_verified = (None, None)
        if value :
            (user_infos_id, user_infos_is_verified) = value
        return user_infos_id, user_infos_is_verified

    @classmethod
    def verify_token(cls, user_id: int):
        query = """
            UPDATE users 
            SET is_verified = TRUE
            WHERE id = %s
            RETURNING id
        """
        return cls._execute(query, (user_id,))

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
            WHERE id = %s RETURNING id
        """
        cls._execute(query, (user_id,))

    @classmethod
    def update_location(
        cls, 
        user_id: int, 
        latitude: float,
        longitude: float,
        injected_cursor = None
    ) -> bool:
        query = """
            UPDATE users 
            SET latitude = %s,longitude = %s
            WHERE id = %s
            RETURNING id
        """
        return cls._execute(query, (latitude, longitude, user_id,), injected_cursor)

    @classmethod
    def update_password(cls, user_id: int, new_password: str) :
        query = """
            UPDATE users 
            SET password_hash = %s 
            WHERE id = %s
            RETURNING id
        """
        password_hash = User.hashing_password(password=new_password)
        return cls._execute(query, (password_hash, user_id))
    
    @classmethod
    def update_email(cls, user_id: int, email: str) :
        query = """
            UPDATE users 
            SET email = %s 
            WHERE id = %s
            RETURNING id
        """
        return cls._execute(query, (email, user_id))
    #     _columns = [
    #     "id", "username", "first_name", "last_name", 
    #     "password_hash", "email", "fame_rating",
    #     "latitude", "longitude", "is_verified"
    # ]
    @classmethod
    def update_user_infos(cls, user_id: int, first_name: str, last_name : str, username: str, birthdate) :
        query = """
            UPDATE users 
            SET
                first_name = %s,
                last_name = %s,
                username = %s,
                birthdate = %s
            WHERE id = %s
            RETURNING id
        """
        return cls._execute(query, (first_name, last_name ,username, birthdate,user_id))

    @classmethod
    def create_user_oauth(cls, user_data: User) -> Optional[User]:
        norm_data = {
            'username' : user_data.username,
            'first_name' : user_data.first_name,
            'last_name' : user_data.last_name,
            'email' : user_data.email,
            'is_verified' : True
        }

        user_id = cls.insert(table_name=cls._table_name, columns=cls._columns_insertion_oauth, data=norm_data)

        return user_id    
    
    @classmethod
    def cleaning_username(cls, username: str):
        text = text.lower().strip()
        return re.sub(r'[^\w+]', '', text)

    @classmethod
    def generate_unique_username(cls, username: str):
        clean_name = cls.cleaning_username(username)
        
        exists = cls.find_by_username(clean_name)
        if not exists:
            return clean_name

        for _ in range(6):
            suffix = "".join(random.choices(string.digits, k=6))
            new_username = f"{clean_name}_{suffix}"
            
            exists = cls.find_by_username(new_username)
            if not exists:
                return new_username

        while not exists:
            new_username = f"{clean_name}".join(random.choices(string.ascii_lowercase + string.digits, k=6))
            exists = cls.find_by_username(new_username)
            if not exists:
                return new_username

    @classmethod
    def find_by_location(cls, id: int,  min_lat: int, max_lat: int, min_lng: int, max_lng: int) -> Optional[User]:
        query = """
            SELECT username, id, latitude, longitude,
            (
                SELECT json_agg(json_build_object('url', up.url, 'is_profile_picture', up.is_profile_picture))
                FROM user_pictures up
                WHERE up.user_id = u.id AND is_profile_picture = TRUE) AS profile_picture_url 
                FROM users u
            WHERE (latitude >= %s AND latitude <= %s) AND (longitude >= %s AND longitude <= %s)
            AND id NOT IN (SELECT blocked_id FROM user_blocks WHERE blocker_id = %s)
            AND id NOT IN (SELECT blocker_id FROM user_blocks WHERE blocked_id = %s)
        LIMIT 100;"""
        rows = cls._fetch_all(query, (min_lat,max_lat, min_lng, max_lng, id, id))
        return rows