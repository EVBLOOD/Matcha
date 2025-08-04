from app.dal.models.user import User
from app.dal.repositories.user_repository import UserRepository
from typing import Optional
import re

class UserService:
    @staticmethod
    def create_user(username: str, email: str,
                    password: str, first_name: str,
                    last_name: str, latitude: Optional[float] = None,
                    longitude: Optional[float] = None) -> Optional[User]:


        if UserRepository.find_by_username(username):
            raise ValueError("Username already taken")
        
        if UserRepository.find_by_email(email):
            raise ValueError("email already taken")

        return UserRepository.create_user(User(
            username=username, 
            email=email,
            password_hash=password,
            first_name=first_name,
            last_name=last_name,
            # longitude=longitude,
            # latitude=latitude 
            insertion_check=True
        ))
    @staticmethod
    def verify_account(token : str) :
        user_id, is_verified = UserRepository.find_by_verification_token(token)
        if is_verified :
            raise ValueError("Account already verified")
        UserRepository.verify_token(user_id)
