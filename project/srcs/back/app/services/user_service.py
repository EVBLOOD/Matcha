from app.dal.models.user import User
from app.dal.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from typing import Optional
import secrets
from app.core.config import Config
from app.services.emailing_service import EmailingService

from app.dal.repositories.user_repository import UserRepository
from app.services.user_interactions_service import UserInteractionsService
from app.services.user_interests_service import UserInterestsService

from zxcvbn import zxcvbn
import os

class UserService:

    _english_words = set()
    dict_path = "/usr/share/dict/words"
    
    if os.path.exists(dict_path):
        with open(dict_path, "r") as f:
            _english_words = {line.strip().lower() for line in f if len(line.strip()) > 3}

    @staticmethod
    def validate_password_strength(password: str, user_inputs: list = None) -> None:
        if user_inputs is None:
            user_inputs = []
        
        password_lower = password.lower()
        
        if password_lower in UserService._english_words:
            raise ValueError("Password cannot be a single common dictionary word.")
        
        # if user_inputs:
        #     for info in user_inputs:
        #         if len(info) > 2 and info.lower() in password_lower:
        #             raise ValueError(f"Password contains personal information")
        
        result = zxcvbn(password, user_inputs=user_inputs)
        
        if result['score'] < 3:
            feedback = result['feedback']
            suggestions = feedback.get('suggestions', [])
            warning = feedback.get('warning', '')
            
            error_msg = "Password too weak. "
            if warning:
                error_msg += warning + " "
            if suggestions:
                error_msg += " ".join(suggestions)
            
            raise ValueError(error_msg)
        
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        if len(password) > 64:
            raise ValueError("Password too long (max 64 characters)")

    @staticmethod
    def create_user(username: str, email: str,
                    password: str, first_name: str,
                    last_name: str, birthdate) -> Optional[User]:


        if UserRepository.find_by_username(username):
            raise ValueError("Username already taken")
        
        if UserRepository.find_by_email(email):
            raise ValueError("email already taken")
        
        UserService.validate_password_strength(
            password, 
            user_inputs=[username, email, first_name, last_name]
        )

        user_data, token_verify, user_id = UserRepository.create_user(User(
            username=username, 
            email=email,
            password_hash=password,
            first_name=first_name,
            last_name=last_name,
            birthdate=birthdate,
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
        if not user_id :
            raise ValueError("token isn't valid!!")
        if is_verified :
            raise ValueError("Account already verified")
        return UserRepository.verify_token(user_id)
    
    @staticmethod
    def resend_verify_token(user_id: int) :
        user = UserRepository.find_by_id(user_id)
        user = User(*user)
        if user.is_verified :
            raise ValueError("Account already verified")
        token = UserRepository.create_verify_token(user_id)
        if token :
            if user_id is not None :
                try :
                    EmailingService.resend_email(user.email, user.username, token)
                except Exception as e :
                    raise ValueError ("Email Not VALID!")
        else :
            return None
        return 1

    @staticmethod
    def change_password(user_id: int, password: str, session_id: str) :
        # TODO: check password 
        user = UserService.get_user(user_id)
        print(user.first_name, flush=True)
        UserService.validate_password_strength(
            password, 
            user_inputs=[user.username, user.email, user.first_name, user.last_name]
        )
        UserRepository.update_password(user_id=user_id, new_password=password)
        print("done", flush=True)
        AuthService.user_session_changed_role(user_id=user_id, session_id=session_id)
        return 1
    
    @staticmethod
    def update_user_infos(user_id: int, username: str, first_name: str, last_name: str, birthdate) :
        try :
            UserRepository.update_user_infos(user_id, first_name, last_name , username, birthdate)
        except Exception as e :
            raise ValueError(str(e)) # unique username
    
    @staticmethod
    def update_user_email_request(user_id: int, email: str, session_id: str ) :
        redis = Config.redis_instence

        user = UserRepository.find_by_email(email)

        if user :
            raise ValueError("Email can't be used!")
        
        token = secrets.token_urlsafe(32)
        key = f"email_change:{email}"
        redis.hset(key, mapping={
            "token": token,
            "user_id": user_id
        })
        redis.expire(key, 3600)
        redis.sadd(f"user_email_change:{user_id}:emails", email)
        user = User(*UserRepository.find_by_id(user_id))

        # TODO: here we should check if the email is valid or reject it
        try :
            EmailingService.send_email_change_confirming(email, user.username, token, session_id, user_id)
        except Exception as e :
            print(e, flush=True)
            # TODO: delete the email change from redis
            raise ValueError ("Email Not VALID!")
            raise ValueError(str(e))

    @staticmethod
    def update_user_email_request_and_infos(user_id: int, username: str, first_name: str, last_name: str, email: str, birthdate, session_id: str) :
        from datetime import datetime, timedelta
        if birthdate:
                min_age_date = datetime.now() - timedelta(days=18*365.25)
                
                if isinstance(birthdate, str):
                    birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
                
                if birthdate > min_age_date.date():
                    raise ValueError("You must be at least 18 years old")

        user = User(*UserRepository.find_by_id(user_id))
        if user.email != email :
            UserService.update_user_email_request(user_id, email, session_id)
        if not (username == user.username and first_name == user.first_name and last_name == user.last_name and birthdate == user.birthdate) :
            UserService.update_user_infos(user_id, username, first_name, last_name, birthdate)
        return 1

    @staticmethod
    def confirm_change(user_id: int, token: str, email: str, session_id: str) -> bool:
        redis = Config.redis_instence
        key = f"email_change:{email}"
        data = redis.hgetall(key)

        if not data or data.get(b"token").decode('utf-8') != token or data.get(b"user_id").decode('utf-8') != user_id:
            return False
        UserRepository.update_email(user_id, email)
        
        redis.delete(key)
        user_emails_key = f"user_email_change:{user_id}:emails"
        redis.delete(user_emails_key)

        AuthService.user_session_changed_role(user_id=user_id, session_id=session_id)
        return True


    @staticmethod
    def get_range_users(user_id: int, min_lat: int, max_lat: int, min_lng: int, max_lng: int) :
        users = UserRepository.find_by_location(user_id, min_lat, max_lat, min_lng, max_lng)
        print(users, flush=True)
        return users
    
    @staticmethod
    def get_user_location(user_id: int) :
        user = User(*UserRepository.find_by_id(user_id))
        return {"latitude": user.latitude, "longitude": user.longitude}


    def get_user(user_id: int) :
        user = User(*UserRepository.find_by_id(user_id))
        return user

    @staticmethod
    def get_user_full_name(user_id: int) :
        user = User(*UserRepository.find_by_id(user_id))
        return user.first_name + " " + user.last_name