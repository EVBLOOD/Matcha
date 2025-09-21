from app.dal.models.user import User
from app.dal.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from typing import Optional
import secrets
from app.core.config import Config
from app.services.emailing_service import EmailingService

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
        # TODO: 
        # The user IP should be shared with the state of him accepting that or not - important
        user_data, token_verify, user_id = UserRepository.create_user(User(
            username=username, 
            email=email,
            password_hash=password,
            first_name=first_name,
            last_name=last_name,
            # longitude=longitude,
            # latitude=latitude 
            insertion_check=True
        ))
        if user_id is not None :
            try :
                EmailingService.send_email_welcoming(user_data.email, user_data.username, token_verify)
            except Exception as e :
                UserRepository.delete(user_id)
                # TODO: remove email from redis record
                raise ValueError ("Email Not VALID!")
        return user_id

    @staticmethod
    def verify_account(token : str) :
        (user_id, is_verified) = UserRepository.find_by_verification_token(token)
        if is_verified :
            raise ValueError("Account already verified")
        UserRepository.verify_token(user_id)
    
    @staticmethod
    def change_password(user_id: int, password: str, session_id: str) :
        # TODO: check password 
        UserRepository.update_password(user_id=user_id, new_password=password)
        AuthService.user_session_changed_role(user_id=user_id, session_id=session_id)
    
    @staticmethod
    def update_user_infos(user_id: int, username: str, first_name: str, last_name: str) :
        try :
            UserRepository.update_user_infos(user_id, first_name, last_name , username)
        except Exception as e :
            raise ValueError(str(e)) # unique username
    
    @staticmethod
    def update_user_email_request(user_id: int, email: str) :
        redis = Config.redis_instence

        user = UserRepository.find_by_email(email)
        if user.id != int(user_id) or email == user.email:
            raise ValueError("Email can't be used!")
        
        token = secrets.token_urlsafe(32)
        print ("email token", email,  token, flush=True)
        key = f"email_change:{email}"
        redis.hset(key, mapping={
            "token": token,
            "user_id": user_id
        })
        redis.expire(key, 3600)
        redis.sadd(f"user_email_change:{user_id}:emails", email)
        # TODO: here we should check if the email is valid or reject it
        try :
            EmailingService.send_email_change_confirming(email, user.username, email)
        except Exception as e :
            # TODO: delete the email change from redis
            raise ValueError ("Email Not VALID!")
            raise ValueError(str(e))


    @staticmethod
    def confirm_change(self, user_id: int, token: str, email: str, session_id: str ) -> bool:
        redis = Config.redis_instence
        key = f"email_change:{email}"
        data = redis.hgetall(key)
        
        if not data or data.get("token") != token or data.get("user_id") != user_id:
            return False
        UserRepository.update_email(user_id, email)
        
        redis.delete(key)
        user_emails_key = f"user_email_change:{user_id}:emails"
        redis.delete(user_emails_key)

        AuthService.user_session_changed_role(user_id=user_id, session_id=session_id)
        return True