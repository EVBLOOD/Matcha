from datetime import datetime, timedelta

import re
import bcrypt

class User:
    def __init__(
        self,
        id: int = None,
        username: str = None,
        first_name: str = None,
        last_name: str = None,
        password_hash: str = None,
        birthdate: datetime = None,
        email: str = None,
        fame_rating: int = 0,
        latitude: float = 0.0,
        longitude: float = 0.0,
        verification_token: str = None,
        is_verified: bool = False,
        last_online: datetime = None,
        created_at: datetime = None,
        insertion_check: bool = False
    ):
        if insertion_check \
              and not self.isvalid_username(username) \
              and not self.isvalid_fullname(first_name, last_name) \
              and not self.isvalid_email(email) and not self.isvalid_password(password_hash):
            raise ValueError
        elif insertion_check is False :
            self.id = id
            self.created_at = created_at
            self.fame_rating = fame_rating
            self.is_verified = is_verified
            self.last_online = last_online
            self.password_hash = password_hash
            self.birthdate = birthdate
        elif insertion_check is True :
            self.password_hash = self.hashing_password(password_hash)
            if birthdate:
                min_age_date = datetime.now() - timedelta(days=18*365.25)
                
                if isinstance(birthdate, str):
                    birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
                
                if birthdate > min_age_date.date():
                    raise ValueError("You must be at least 18 years old")
            self.birthdate = birthdate
        self.verification_token = verification_token
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.latitude = latitude
        self.longitude = longitude

    def isvalid_username(self, username: str) :
        username_regex = r"^[a-zA-Z0-9_-]{3,16}$"
        return re.match(username_regex, username) and len(username) < 16
    def isvalid_fullname(self, first_name: str, last_name: str) :
        name_regex = r"^[a-zA-Z' -]+$"
        return re.match(name_regex, first_name) and re.match(name_regex, last_name) \
             and len(first_name) <= 50 and len(last_name) <= 50


    def isvalid_email(self, email: str):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) and len(email) < 255
    
    @staticmethod
    def hashing_password(password) :
        return bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    def isvalid_password(self, password) :
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+-=])(?=\S+$).{8,64}$"
        return re.match(password_regex, password)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password_hash,
            "fame_rating": self.fame_rating,
            "last_online": self.last_online.isoformat() if self.last_online else None,
            "is_verified": self.is_verified
        }