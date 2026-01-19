from app.dal.repositories.user_repository import UserRepository, User
import bcrypt
from flask_jwt_extended import create_refresh_token, create_access_token
from app.core.config import Config
import uuid
import secrets
from app.dal.repositories.profile_repository import ProfileRepository
from app.services.emailing_service import EmailingService


class AuthService :
    @staticmethod
    def verify_is_verified(user_id: int) :

        try :
            is_verified = UserRepository.find_by_id(id=user_id, what="is_verified")
            return is_verified and is_verified[0]
        except Exception as e :
            return False

    @staticmethod
    def verify_user(username: str, password: str) :
        try :
            user = UserRepository.find_by_username(username=username)
            if not user.password_hash :
               raise ValueError("Please log-in with your social account or reset your password to create one")
            if bcrypt.checkpw(password.encode(), user.password_hash.encode()) :
                return user
        except Exception as e :
            return None
        return None
    
    @classmethod
    def generate_token(cls, id: int, username: int, request) :

        session_id = str(uuid.uuid4())
        access_token = create_access_token(identity=str(session_id), 
                                           additional_claims={"user_id": id, "username": username})
        refresh_token = create_refresh_token(identity=str(id))

        cls.create_session(session_id, id, username, request)
        return access_token, refresh_token


    @classmethod
    def create_session(cls, session_id, user_id, username, request):
        redis = Config.redis_instence
        user_version = redis.get(f"user:{user_id}:auth_version") or uuid.uuid4().hex
        redis.set(f"user:{user_id}:auth_version", user_version)
        redis.hset(f"session:{session_id}", mapping={
            "user_id": user_id,
            "username": username,
            "ip": request.remote_addr,
            "auth_version": user_version,
        })
        redis.expire(f"session:{session_id}", 3600*24*7)
        redis.sadd(f"user:{user_id}:sessions", session_id) # set of sessions for a user


        if ProfileRepository.find_profile_exists(user_id) :
            redis.set(f"user:{user_id}:profile_complete", "1")
        else :
            redis.set(f"user:{user_id}:profile_complete", "0")

        return session_id

    def user_session_changed_role(user_id, session_id = None):
        redis = Config.redis_instence
        user_version = uuid.uuid4().hex
        redis.set(f"user:{user_id}:auth_version", user_version)

        if session_id:
            redis.hset(f"session:{session_id}", "auth_version", user_version)



    @classmethod
    def validate_token(cls, user_id, session_id):
        expired, sessions = cls.find_user_session_nt_valid(user_id, session_id)
        if len(sessions) == 0 :
            return ("Not authorized", 403)
        if expired :
            return ("unvalid token", 401)

        return ("Success", 200)

    @classmethod
    def find_user_session_nt_valid(cls, user_id, session_id):
        redis = Config.redis_instence

        current_auth_version = redis.get(f"user:{user_id}:auth_version")

        if current_auth_version:
            current_auth_version = current_auth_version.decode()

        session_key = f"session:{session_id}"
        session_data = redis.hgetall(session_key)
        if not session_data:
            return False, []
        
        session_user_id = session_data.get(b"user_id")
        session_auth_version = session_data.get(b"auth_version")

        if not session_user_id or session_user_id.decode() != str(user_id):
            return False, []

        if session_auth_version is None or session_auth_version.decode() != current_auth_version:
            return True, []

        return False, [1]


    @classmethod
    def logout(cls, session_id, user_id):
        redis = Config.redis_instence
        redis.delete(f"session:{session_id}")
        redis.srem(f"user:{user_id}:sessions", session_id)

    @classmethod
    def reset_password(cls, user_input) :
        # if "@" not in user_input :
        #     user = UserRepository.find_by_username(username=user_input)
        # else :
        #     user = UserRepository.find_by_email(email=user_input)
        user = UserRepository.find_by_email(email=user_input)
        if user is None :
            raise ValueError("Email or username is incorrect")
        AuthService.add_reset_token(email=user.email, user_id=user.id, username=user.username, )

    
    @staticmethod
    def add_reset_token(user_id: str, email: str, username: str, ):
        redis = Config.redis_instence
        token = secrets.token_urlsafe(32)

        try :
            EmailingService.send_email_forgoten_pass(email, username, token)
            redis.setex(f"pwd_reset:{token}", 3600, user_id)
        except Exception as e :
            raise ValueError ("Email Not VALID!")

    @staticmethod
    def check_token(token):
        redis = Config.redis_instence
        user_id = redis.get(f"pwd_reset:{token}")
        return user_id

    @staticmethod
    def check_and_reset_token(token, new_password):
        redis = Config.redis_instence
        user_id = redis.getdel(f"pwd_reset:{token}")

        if user_id is None :
            raise ValueError("Invalid/used token")

        if not UserRepository.update_password(int(user_id), new_password):
            raise ValueError("Password update failed")

        user_version = uuid.uuid4().hex
        redis.set(f"user:{user_id}:auth_version", user_version)
        return user_id

    @staticmethod
    def update_profile_profile_completion(user_id: str) :
        redis = Config.redis_instence
        redis.set(f"user:{user_id}:profile_complete", "1")

    @staticmethod
    def check_profile_completion(user_id: str) :
        redis = Config.redis_instence

        profile_complete = redis.get(f"user:{user_id}:profile_complete")
        if profile_complete and profile_complete.decode() == "1":
            return True
        else :
            return False

