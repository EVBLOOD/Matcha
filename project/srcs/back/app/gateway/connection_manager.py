from app.core.config import Config
from flask import jsonify
from functools import wraps
from flask import request
from flask_socketio import disconnect, join_room, ConnectionRefusedError, leave_room
import json
from flask_jwt_extended import decode_token
from app.core.security import AuthService, Security
# from app.services.user_service import get_user_contacts
from flask_socketio import emit

from app.services.user_interactions_service import UserInteractionsService
from app.services.profile_service import ProfileService
from app.services.notifications_service import NotificationService
from app.dal.repositories.user_repository import UserRepository
from app.services.profile_views_service import ProfileViewsService
from app.services.user_blocks_service import UserBlocksService
from app.services.chat_service import ChatService

class ConnectionManager :

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
        join_room(f"Notifs_user_{user_id}")
        emit('connected', {user_id: "Online"}, room=f"online_user_{user_id}")

    
    @staticmethod
    def disconnect_user(sid: str):
        redis = Config.redis_instence
        user_id = redis.hget("ws:connections", f"sid:{sid}")
        if not user_id:
            return
            
        user_id = int(user_id)
        
        redis.hdel("ws:connections", f"sid:{sid}")
        redis.srem(f"ws:user:{user_id}:sockets", sid)
        
        leave_room(f"Notifs_user_{user_id}", sid=sid)
        leave_room(f"online_user_{user_id}", sid=sid)

        cursor = 0
        pattern = "chat:private_rooms:*"
        while True:
            cursor, keys = redis.scan(cursor, match=pattern, count=100)
            for key in keys:
                if redis.sismember(key, sid):
                    redis.srem(key, sid)
                    room_name = key.decode().replace("chat:private_rooms:", "")
                    leave_room(room_name, sid=sid)
            if cursor == 0:
                break
        if redis.scard(f"ws:user:{user_id}:sockets") == 0:
            redis.delete(f"ws:user:{user_id}:online")
            UserRepository.update_last_online(user_id)

        emit('connected', {user_id: "Disconnected"}, room=f"online_user_{user_id}")

    @staticmethod
    def is_user_online(user_id: int, current_id: int) -> bool:
        block_status = UserBlocksService.get_blocks_status(user_id, current_id)
        if block_status :
            return False
        redis = Config.redis_instence
        join_room(f"online_user_{user_id}")
        is_online = bool(
            redis.exists(f"ws:user:{user_id}:online")
        )
        if not is_online :
            response = UserRepository.find_by_id(user_id, 'last_online')
            return response[0]
        return is_online

    @staticmethod
    def interact_with_user(user_id: int, dst_id: int, type: str) -> bool:
        if user_id == dst_id :
            return
        is_connection = UserInteractionsService.get_user_interactions(user_id, dst_id)
        block_status = UserBlocksService.get_blocks_status(user_id, dst_id)
        conversation_id = None
        type_response = None
        if not block_status and type == "Like" :
            UserInteractionsService.insert_user_interactions(dst_id, user_id)
            type_response = "like"
            if is_connection :
                type_response = "match"
                conversation_id = ChatService.create_conversation(dst_id, user_id)
        elif not block_status and type == "Dislike" :
            done = UserInteractionsService.remove_user_interactions(dst_id, user_id)
            if done and is_connection :
                type_response = "unmatch"
        elif not block_status and type == "Block" :
            if is_connection :
                UserInteractionsService.remove_user_interactions(dst_id, user_id)
                UserInteractionsService.remove_user_interactions(user_id, dst_id)
            UserBlocksService.insert_user_blocks(dst_id, user_id)
            return
        elif block_status and type == "Unblock" :
            UserBlocksService.remove_user_blocks(dst_id, user_id)
        elif not block_status:
            type_response = "view"
            ProfileViewsService.insert_profile_views(dst_id, user_id)
        else :
            return
        if block_status :
            return
        try :
            user = ProfileService.get_user_profile_basic(user_id)
        except :
            return
        if type_response :
            done = NotificationService.create_notification(dst_id, type_response, user_id)
            if done :
                if conversation_id :
                    emit('notify', {"source_id": user_id, "dst_id": dst_id, "user": user, "type": type_response, "conversation_id": conversation_id}, room=f"Notifs_user_{dst_id}")
                else :
                    emit('notify', {"source_id": user_id, "dst_id": dst_id, "user": user, "type": type_response}, room=f"Notifs_user_{dst_id}")
    #     [ ] On Message received.



        redis = Config.redis_instence
        # update this
        # join_room(f"online_user_{user_id}")
        return bool(
            redis.exists(f"ws:user:{user_id}:online")
        )

    @staticmethod
    def get_number_of_notifs(user_id: int):
        try :
            return NotificationService.get_number_unreaded_notification(user_id)
        except :
            return 0

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
                    decoded_token = Security.jwt._decode_jwt_from_config(token)
                    message, status = AuthService.validate_token(decoded_token["user_id"], decoded_token["sub"])
                    if status != 200 :
                        raise Exception(message)
                    # This maybe will be moved down when working with the admin role
                    # if check_profile and not AuthService.check_profile_completion(decoded_token["user_id"]) :
                    #     raise Exception("profile completion required")
                    request.user_id = decoded_token["user_id"]
                except Exception as e:
                    print(f"Socket authentication failed: {str(e)}", flush=True)
                    if f.__name__ == 'on_connect' :
                        raise ConnectionRefusedError(str(e))
                    elif f.__name__ == 'on_disconnect' :
                        return
                    else :
                        emit('auth_error', {'message': str(e)})
                        disconnect()
                    return
                return f(*args, **kwargs)
            return wrapped
        return decorator
