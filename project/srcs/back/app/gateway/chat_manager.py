from app.core.config import Config
from flask import jsonify
from functools import wraps
from flask import request
from flask_socketio import disconnect, join_room, ConnectionRefusedError, leave_room
import json
from flask_jwt_extended import decode_token
from app.core.security import AuthService, Security
from app.services.user_interactions_service import UserInteractionsService
from app.services.chat_service import ChatService
from flask_socketio import emit
from typing import Set


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
            return {"You aren't allowd to reach this person!"}
        redis = Config.redis_instence
        room_name = ChatManager._get_canonical_room_name(user_id, other_id)

        if redis.sismember(f"chat:private_rooms:{room_name}", socket_id):
            return
        join_room(room_name)
        redis.sadd(f"chat:private_rooms:{room_name}", socket_id)

    @staticmethod
    def leave_private_room(user_id: str, other_id: str, socket_id: str):
        if not UserInteractionsService.are_users_connected(other_id, user_id) :
            return {"You aren't allowd to reach this person!"}
        redis = Config.redis_instence
        room_name = ChatManager._get_canonical_room_name(user_id, other_id)
        
        leave_room(room_name)
        redis.srem(f"chat:room_{room_name}", socket_id)

    @staticmethod
    def broadcast_message(sender: str, receiver: str, message: str, socket_id: str):
        if not UserInteractionsService.are_users_connected(sender, receiver) :
            return {"You aren't allowd to reach this person!"}

        redis = Config.redis_instence
        private_room = ChatManager._get_canonical_room_name(sender, receiver)
        message_id = ChatService.send_message(sender, receiver, message)
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
            emit(
                'new_message_notification', 
                {"sender": sender, "count_change": 1}, 
                room=notify_room
            )
        return message_id
    
    @staticmethod
    def join_call(caller_id: str, reciever_id, socket_id) :
        if not UserInteractionsService.are_users_connected(caller_id, reciever_id["user_id"]) :
            return {"You aren't allowd to reach this person!"}
        
        private_room = ChatManager._get_canonical_room_name(reciever_id["user_id"], caller_id)

        # redis again
        emit('video_signal', reciever_id, room=private_room, include_self=False)

