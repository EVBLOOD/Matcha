from app.core.config import Config
from flask import jsonify
from functools import wraps
from flask import request
from flask_socketio import disconnect, join_room, ConnectionRefusedError, leave_room
import json
from flask_jwt_extended import decode_token
from app.core.security import AuthService, Security
from flask_socketio import emit
from datetime import datetime, timezone

from app.services.user_interactions_service import UserInteractionsService
from app.services.profile_service import ProfileService
from app.services.notifications_service import NotificationService
from app.dal.repositories.user_repository import UserRepository
from app.services.profile_views_service import ProfileViewsService
from app.services.user_blocks_service import UserBlocksService
from app.services.chat_service import ChatService
from app.services.dates_service import DatesService


class ConnectionManager :
    DISCONNECT_RUN = """
        redis.call('HDEL', KEYS[1], 'sid:' .. ARGV[1])
        redis.call('SREM', KEYS[2], ARGV[1])
        local remaining = redis.call('SCARD', KEYS[2])
        if remaining == 0 then
            redis.call('DEL', KEYS[3])
        end
        return remaining
        """

    CONNECT_RUN = """
        redis.call('HSET', KEYS[1], 'sid:' .. ARGV[1], ARGV[2])
        local is_new_to_set = redis.call('SADD', KEYS[2], ARGV[1])
        local already_online = redis.call('EXISTS', KEYS[3])
        redis.call('SETEX', KEYS[3], ARGV[3], '1')
        return (already_online == 0) and 1 or 0
        """

    TTL = 60

    @staticmethod
    def connect_user(user_id: int, sid: str):

        redis = Config.redis_instence

        is_first_connection = redis.eval(
            ConnectionManager.CONNECT_RUN, 3, 
            "ws:connections",
            f"ws:user:{user_id}:sockets",
            f"ws:user:{user_id}:online",
            sid, user_id, ConnectionManager.TTL
        )

        join_room(f"online_user_{user_id}")
        join_room(f"Notifs_user_{user_id}")

        if is_first_connection:
            emit('user_status_change', 
                 {"user_id": user_id, "status": "online"}, 
                 room=f"online_user_{user_id}", 
                 include_self=False)
    
    @staticmethod
    def disconnect_user(sid: str):
        redis = Config.redis_instence
        
        user_id_bytes = redis.hget("ws:connections", f"sid:{sid}")
        if not user_id_bytes:
            return

        user_id = int(user_id_bytes)

        remaining_sockets = redis.eval(
            ConnectionManager.DISCONNECT_RUN, 3,
            "ws:connections",
            f"ws:user:{user_id}:sockets",
            f"ws:user:{user_id}:online",
            sid
        )

        if remaining_sockets == 0:
            last_seen = datetime.now(timezone.utc).isoformat()
            UserRepository.update_last_online(user_id)
            emit('user_status_change', 
                 {"user_id": user_id, "status": last_seen}, 
                 room=f"online_user_{user_id}")

        leave_room(f"online_user_{user_id}", sid=sid)
        leave_room(f"Notifs_user_{user_id}", sid=sid)
    
    @staticmethod
    def heartbeat(user_id: int):
        redis = Config.redis_instence
        redis.expire(f"ws:user:{user_id}:online", ConnectionManager.TTL)
        redis.expire(f"ws:user:{user_id}:sockets", ConnectionManager.TTL)

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
            return str(response[0])
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
            conversation_id = 1
            if is_connection :
                type_response = "match"
                conversation_id = ChatService.create_conversation(dst_id, user_id)
        elif not block_status and type == "Dislike" :
            done = UserInteractionsService.remove_user_interactions(dst_id, user_id)
            if done: 
                conversation_id = -1
                type_response = "dislike"
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
            if type_response != 'dislike' :
                done = NotificationService.create_notification(dst_id, type_response, user_id)
            else :
                done = 1
            if done :
                if conversation_id :
                    emit('notify', {"source_id": user_id, "dst_id": dst_id, "user": user, "type": type_response, "conversation_id": conversation_id}, room=f"Notifs_user_{dst_id}")
                    emit('notify', {"source_id": user_id, "dst_id": dst_id, "user": user, "type": type_response, "conversation_id": conversation_id}, room=f"Notifs_user_{user_id}")
                else :
                    emit('notify', {"source_id": user_id, "dst_id": dst_id, "user": user, "type": type_response}, room=f"Notifs_user_{dst_id}")



        redis = Config.redis_instence

        return bool(
            redis.exists(f"ws:user:{user_id}:online")
        )

    def propose_date(user_id, body):
        try :

            date_id = DatesService.propose_date(
                proposer_id=user_id,
                partner_id=body['partner_id'],
                location=body['location'],
                datetime_str=body['datetime_str'],
                description=body['description']
            )
            user = ProfileService.get_user_profile_basic(body['partner_id'])
            emit('notify', {"date_id": date_id, "source_id": user_id, "dst_id": body['partner_id'], "user": user, "type": "Date Propose"}, room=f"Notifs_user_{user_id}")
            emit('notify', {"date_id": date_id, "source_id": user_id, "dst_id": body['partner_id'], "user": user, "type": "Date Propose"}, room=f"Notifs_user_{body['partner_id']}")
        except Exception as e:
            return False
        return date_id


    def respond_to_date(user_id, body):
        try :
            dst_id = DatesService.respond_to_date(
                date_id=body['event_id'],
                responder_id=user_id,
                status=body['status']
            )
            user = ProfileService.get_user_profile_basic(dst_id)
            emit('notify', {"date_id": body['event_id'], "source_id": user_id, "dst_id": dst_id, "user": user, "type": f"Date {body['status']}"}, room=f"Notifs_user_{dst_id}")
            emit('notify', {"date_id": body['event_id'], "source_id": user_id, "dst_id": dst_id, "user": user, "type": f"Date {body['status']}"}, room=f"Notifs_user_{user_id}")
        except :
            return False
        return True


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
                if f.__name__ == 'on_disconnect':
                    return f(*args, **kwargs)
                try :
                    token = (request.headers.get('Authorization') and 
                                    request.headers.get('Authorization').split(' ')[1])
                    if not token:
                        raise Exception("Missing authentication token")
                    decoded_token = Security.jwt._decode_jwt_from_config(token)
                    message, status = AuthService.validate_token(decoded_token["user_id"], decoded_token["sub"])
                    if status != 200 :
                        raise Exception(message)
                    if not AuthService.check_profile_completion(decoded_token["user_id"]) :
                        raise Exception("profile completion required")
                    request.user_id = decoded_token["user_id"]
                except Exception as e:
                    if f.__name__ == 'on_connect' :
                        return False
                    else :
                        try :
                            emit('auth_error', {'message': str(e)})
                            disconnect()
                        except :
                            pass
                    return None
                return f(*args, **kwargs)
            return wrapped
        return decorator
