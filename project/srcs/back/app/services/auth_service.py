from app.dal.repositories.user_repository import UserRepository
import bcrypt
from flask_jwt_extended import create_refresh_token, create_access_token


class AuthService :
    @staticmethod
    def verify_user(username: str, password: str) :
        try :

            user = UserRepository.find_by_username(username=username)
            
            if bcrypt.checkpw(password.encode(), user.password_hash.encode()) :
                return user
        except Exception as e :
            print(e, flush=True)
            return None
        return None
    
    @staticmethod
    def generate_token(id: int, username: str) :
        access_token = create_access_token(identity=id, additional_claims={"username": username})
        refresh_token = create_refresh_token(identity=id)
        return access_token, refresh_token
