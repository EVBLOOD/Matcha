from datetime import datetime
from typing import Optional

class User:
    def __init__(
        self,
        id: int = None,
        # id: Optional[int] = None,
        username: str = None,
        first_name: str = None,
        last_name: str = None,
        password_hash: str = None,
        email: str = None,
        fame_rating: int = 0,
        # latitude: float = None,
        # longitude: float = None,
        latitude: float = 0.0,
        longitude: float = 0.0,
        is_verified: bool = False,
        last_online: datetime = None,
        created_at: datetime = None,
        insertion_check: bool = False
    ):
        if insertion_check \
              and not self.isvalid_username(username) \
              and not self.isvalid_fullname(first_name, last_name) \
              and not self.isvalid_email(email):
            raise ValueError
        elif insertion_check is False :
            self.id = id
            self.created_at = created_at
            self.fame_rating = fame_rating
            self.is_verified = is_verified
            self.last_online = last_online

        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        # self.password_hash = self.hash_password(password_hash)
        self.password_hash = password_hash
        self.latitude = latitude
        self.longitude = longitude

    def isvalid_username(self, username: str) :
        return username != ""
    def isvalid_fullname(self, first_name: str, last_name: str) :
        return first_name != "" and last_name != ""
    def isvalid_email(self, email: str):
        return email != ""
    # def full_name(self) -> str:
    #     return f"{self.first_name} {self.last_name}"

    # def to_dict(self) -> dict:
    #     return {
    #         "id": self.id,
    #         "username": self.username,
    #         "email": self.email,
    #         "fame_rating": self.fame_rating,
    #         "last_online": self.last_online.isoformat() if self.last_online else None,
    #         "is_verified": self.is_verified
    #     }