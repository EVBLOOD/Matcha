from app.core.config import Config
from flask import jsonify
from functools import wraps
from flask import request
from flask_socketio import disconnect, join_room, ConnectionRefusedError, leave_room
import json
from flask_jwt_extended import decode_token
from app.core.security import AuthService, Security
from app.services.profile_service import ProfileService
from app.services.user_interactions_service import UserInteractionsService
from app.services.chat_service import ChatService
from flask_socketio import emit
from typing import Set
import uuid
import threading
import time

from app.services.user_blocks_service import UserBlocksService

class ChatManager :

    # Just helpers
    @staticmethod
    def _get_canonical_room_name(user1: str, user2: str) -> str:
        return f"private_{'_'.join(sorted([str(user1), str(user2)]))}"

    @staticmethod
    def _get_user_room_name(user_id: str) -> str:
        return f"user_{user_id}_notify"
    
    # Main functions
    @staticmethod
    def connect_user_socket(user_id: str, socket_id: str):
        redis = Config.redis_instence
        room_name = ChatManager._get_user_room_name(user_id)
        
        join_room(room_name)
        redis.sadd(f"chat:user_sockets:{user_id}", socket_id)
        
    @staticmethod
    def disconnect_user_socket(user_id: str, socket_id: str):
        redis = Config.redis_instence
        room_name = ChatManager._get_user_room_name(user_id)
        
        leave_room(room_name)
        redis.srem(f"chat:user_sockets:{user_id}", socket_id)

    @staticmethod
    def join_private_room(user_id: str, other_id: str, socket_id: str):
        if not UserInteractionsService.are_users_connected(other_id, user_id) :
            return {"error":"You aren't allowed to reach this person!"}
        redis = Config.redis_instence
        room_name = ChatManager._get_canonical_room_name(user_id, other_id)

        if redis.sismember(f"chat:private_rooms:{room_name}", socket_id):
            return
        join_room(room_name)
        redis.sadd(f"chat:private_rooms:{room_name}", socket_id)

    @staticmethod
    def leave_private_room(user_id: str, other_id: str, socket_id: str):
        # if not UserInteractionsService.are_users_connected(other_id, user_id) :
        #     return {"error": "You aren't allowed to reach this person!"}
        redis = Config.redis_instence
        room_name = ChatManager._get_canonical_room_name(user_id, other_id)
        
        leave_room(room_name)
        redis.srem(f"chat:room_{room_name}", socket_id)

    @staticmethod
    def broadcast_message(sender: str, receiver: str, message: str, socket_id: str):
        if not UserInteractionsService.are_users_connected(sender, receiver) :
            return {"error":"You aren't allowed to reach this person!"}

        redis = Config.redis_instence
        private_room = ChatManager._get_canonical_room_name(sender, receiver)
        (chat_id, message_id) = ChatService.send_message(sender, receiver, message)
        emit(
            'message_chat', 
            {"text": message, "sender": sender, "id": message_id}, 
            room=private_room
        )

        receiver_sockets: Set[bytes] = redis.smembers(f"chat:user_sockets:{receiver}")
        active_viewers: Set[bytes] = redis.smembers(f"chat:private_rooms:{private_room}")
        sockets_needing_notif = receiver_sockets - active_viewers

        if sockets_needing_notif:
            # TODO: correct this later
            notify_room = ChatManager._get_user_room_name(receiver)
            # user = payload.avatar, payload.FromId, payload.username
            try :
                user = ProfileService.get_user_profile_basic(sender)
            except:
                return False
            emit(
                'new_message_notification', 
                {"sender": sender, "count_change": 1, 'user_data': user, "conv": chat_id}, 
                room=notify_room
            )
        return message_id

    @staticmethod
    def get_number_of_messages(user_id: int):
        try :
            out = ChatService.get_number_unreaded_messages(user_id)[0]
            print(out, flush=True)
            return out
        except :
            return 0

    @staticmethod
    def cleanup_call(user_id):
        redis = Config.redis_instence
        
        call_id = redis.get(f"call:user:{user_id}")
        if not call_id:
            return

        call_data = redis.hgetall(f"call:{call_id}")
        if not call_data:
            redis.delete(f"call:user:{user_id}")
            return

        caller_id = call_data.get("caller")
        receiver_id = call_data.get("receiver")
        
        other_id = receiver_id if str(caller_id) == str(call_data) else caller_id

        if other_id :
            Config.socket_instence.emit("video_signal", {"type": "hangup"}, room=f"user_{other_id}_notify", namespace='/chat')

        pipe = redis.pipeline()
        pipe.delete(f"call:{call_id}")
        pipe.delete(f"call:user:{caller_id}")
        pipe.delete(f"call:user:{receiver_id}")
        pipe.execute()

    @staticmethod
    def handle_call_timeout(call_id, caller_id, receiver_id):
        redis = Config.redis_instence
        call_data = redis.hgetall(f"call:{call_id}")
        
        if call_data and call_data.get("status") == "ringing":
            ChatManager.cleanup_call(caller_id)
            
            timeout_payload = {"type": "timeout", "message": "No answer"}
            Config.socket_instence.emit("video_signal", timeout_payload, room=f"user_{caller_id}_notify", namespace='/chat')
            Config.socket_instence.emit("video_signal", timeout_payload, room=f"user_{receiver_id}_notify", namespace='/chat')

    @staticmethod
    def handle_heartbeat(user_id):
        redis = Config.redis_instence
        call_id = redis.get(f"call:user:{user_id}")
        
        if call_id:
            pipe = redis.pipeline()
            pipe.expire(f"call:{call_id}", 60)
            pipe.expire(f"call:user:{user_id}", 60)
            
            call = redis.hgetall(f"call:{call_id}")
            if call:
                other = call["receiver"] if call["caller"] == str(user_id) else call["caller"]
                pipe.expire(f"call:user:{other}", 60)
            pipe.execute()

    @staticmethod 
    def handle_calls(caller_id: str, data, socket_id):
        receiver_id = data.get('user_id')
        signal_type = data.get('type')

        redis = Config.redis_instence

        if signal_type == 'offer' and not UserInteractionsService.are_users_connected(caller_id, receiver_id):
            return {"status": "error", "message": "Connection required"}

        if signal_type == 'hangup':
            ChatManager.cleanup_call(caller_id)
            return

        if signal_type == 'candidate':
            emit('video_signal', data, room=f"user_{receiver_id}_notify", include_self=False)
            return
        
        if not redis.exists(f"ws:user:{receiver_id}:online"):
            emit("video_signal", {"type": "offline"}, room=f"user_{caller_id}_notify")
            return

        existing_call_id = redis.get(f"call:user:{caller_id}")

        if existing_call_id:
            call_data = redis.hgetall(f"call:{existing_call_id}")
            
            is_same_call = (
                (call_data.get("caller") == str(caller_id) and call_data.get("receiver") == str(receiver_id)) or 
                (call_data.get("caller") == str(receiver_id) and call_data.get("receiver") == str(caller_id))
            )
            
            if is_same_call:
                if signal_type == 'answer':
                    redis.hset(f"call:{existing_call_id}", "status", "active")
                
                emit('video_signal', data, room=f"user_{receiver_id}_notify", include_self=False)
                return
            else:
                emit("video_signal", {"type": "busy"}, room=f"user_{caller_id}_notify")
                return

        call_id = uuid.uuid4().hex

        if not redis.set(f"call:user:{receiver_id}", call_id, nx=True, ex=300):
            emit("video_signal", {"type": "busy"}, room=f"user_{caller_id}_notify")
            return

        if not redis.set(f"call:user:{caller_id}", call_id, nx=True, ex=300):
            redis.delete(f"call:user:{receiver_id}")
            emit("video_signal", {"type": "busy"}, room=f"user_{caller_id}_notify")
            return

        redis.hset(f"call:{call_id}", mapping={
            "caller": caller_id,
            "receiver": receiver_id,
            "status": "ringing",
            "started_at": int(time.time())
        })
        redis.expire(f"call:{call_id}", 300)

        profile = ProfileService.get_user_profile_basic(caller_id, True)
        signal_payload = data.copy()
        signal_payload.update({
            "sender_id": caller_id,
            "sender_name": profile['user']['name'],
            "sender_avatar": profile['pictures'][0]['url'] if profile['pictures'] else None
        })

        threading.Timer(15.0, ChatManager.handle_call_timeout, 
                        args=[call_id, caller_id, receiver_id]).start()

        emit('video_signal', signal_payload, room=f"user_{receiver_id}_notify", include_self=False)

