from app.dal.repositories.user_repository import UserRepository
import bcrypt
from flask_jwt_extended import create_refresh_token, create_access_token
from app.core.config import Config
import uuid

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
    
    @classmethod
    def generate_token(cls, id: int, username: int, request) :

        session_id = str(uuid.uuid4())
        access_token = create_access_token(identity=str(session_id), 
                                           additional_claims={"user_id": id,"username": username})
        refresh_token = create_refresh_token(identity=str(id))

        cls.create_session(session_id, id, username, request)
        return access_token, refresh_token



    @classmethod
    def create_session(cls, session_id, user_id, username, request):
        redis = Config.redis_instence

        redis.hset(f"session:{session_id}", mapping={
            "user_id": user_id,
            "username": username,
            "ip": request.remote_addr,
            "valid": 1
        })
        redis.expire(f"session:{session_id}", 3600*24*7)
        return session_id

    def user_session_changed_role(session_id):
        redis = Config.redis_instence
        redis.hset(f"session:{session_id}", "valid", 0)
        redis.expire(f"session:{session_id}", (3600 / 60) * 5)

    @classmethod
    def validate_token(cls, user_id, session_id):
        expired, sessions = cls.find_user_sessions_nt_valid(user_id, session_id)
        if len(sessions) == 0 :
            return ("Not authorized", 401)
        if expired :
            return ("unvalid token", 401)

        return ("Success", 200)

    @classmethod
    def find_user_sessions_nt_valid(cls, user_id, session_id):
        redis = Config.redis_instence
        found_currect = True
        sessions = []
        
        for key in redis.scan_iter("session:*") :
            if key.decode('utf-8') == str(session_id):
                found_currect = True
            if redis.hget(key, "user_id").decode('utf-8') == str(user_id) :
                print("found!", flush=True)
                sessions.append(redis.hgetall(key))
                if redis.hget(key, "valid").decode('utf-8') == str(0) :
                    return True, sessions

        return (False or found_currect), sessions


    @classmethod
    def logout(cls, session_id):
        redis = Config.redis_instence
        redis.delete(f"session:{session_id}")
