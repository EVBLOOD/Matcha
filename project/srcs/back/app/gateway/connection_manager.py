from app.core.config import Config
from flask import jsonify
from functools import wraps
from flask import request
from flask_socketio import disconnect
import json
from flask_jwt_extended import decode_token
from app.core.security import AuthService, Security


class ConnectionManager:

    @staticmethod
    def connect_user(user_id: int, sid: str):
        redis = Config.redis_instence
        redis.hset(
            f"ws:connections", 
            f"sid:{sid}", 
            user_id
        )
        redis.sadd(
            f"ws:user:{user_id}:sockets", 
            sid
        )
        
        redis.set(
            f"ws:user:{user_id}:online", 
            "1"
        )
        
        # redis.publish(
        #     "ws:presence", 
        #     json.dumps(({
        #         "user_id": user_id,
        #         "status": "online"
        #     }))
        # )
    
    @staticmethod
    def disconnect_user(sid: str):
        redis = Config.redis_instence
        user_id = redis.hget("ws:connections", f"sid:{sid}")
        if not user_id:
            return
            
        user_id = int(user_id)
        
        redis.hdel("ws:connections", f"sid:{sid}")
        redis.srem(f"ws:user:{user_id}:sockets", sid)
        
        if redis.scard(f"ws:user:{user_id}:sockets") == 0:
            redis.delete(f"ws:user:{user_id}:online")
            
            redis.publish(
                "ws:presence",
                jsonify({
                    "user_id": user_id,
                    "status": "offline"
                })
            )

    @staticmethod
    def is_user_online(user_id: int) -> bool:
        redis = Config.redis_instence
        return bool(
            redis.exists(f"ws:user:{user_id}:online")
        )
    
    @staticmethod
    def socket_guard(required_roles=None, check_profile=True):
        def decorator(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                try :
                    token = (request.headers.get('Authorization') and 
                                    request.headers.get('Authorization').split(' ')[1])
                    if not token:
                        raise Exception("Missing authentication token")
                    # decoded_token = decode_token(token)
                    decoded_token = Security.jwt._decode_jwt_from_config(token)
                    print (decoded_token, flush=True)
                    message, status = AuthService.validate_token(decoded_token["user_id"], decoded_token["sub"])
                    if status != 200 :
                        raise Exception(message)
                    # # This maybe will be moved down when working with the admin role
                    if check_profile and not AuthService.check_profile_completion(decoded_token["user_id"]) :
                        raise Exception("profile completion required")
                    request.user_id = decoded_token["user_id"]
                except Exception as e:
                    print(f"Socket authentication failed: {str(e)}", flush=True)
                    disconnect()
                    return 
                return f(*args, **kwargs)
            return wrapped
        return decorator
