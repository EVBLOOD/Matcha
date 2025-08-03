from repositories.user_repository import UserRepository, User
from typing import Optional
import re

class UserService:
    @staticmethod
    def create_user(username: str, email: str) -> Optional[User]:
        """Validates and creates a user."""
        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")

        # Check for duplicate username/email (example)
        if UserRepository.username_exists(username):
            raise ValueError("Username already taken")

        # Create and return the user
        return UserRepository.insert(User(
            id=None,
            username=username,
            email=email
        ))