from datetime import datetime
from typing import Optional

class User:
    def __init__(
        self,
        id: int = None,
        username: str = None,
        first_name: str = None,
        last_name: str = None,
        password_hash: str = None,
        email: str = None,
        fame_rating: int = 0,
        latitude: float = None,
        longitude: float = None,
        is_verified: bool = False,
        last_online: datetime = None,
        created_at: datetime = None
    ):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = password_hash
        self.email = email
        self.fame_rating = fame_rating
        self.latitude = latitude
        self.longitude = longitude
        self.is_verified = is_verified
        self.last_online = last_online
        self.created_at = created_at

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