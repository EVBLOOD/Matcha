from flask_socketio import Namespace
from flask import request
from app.gateway.connection_manager import ConnectionManager
from app.gateway.chat_manager import ChatManager
from flask_socketio import disconnect, emit
import json

class ChatGateway(Namespace):

    @ConnectionManager.socket_guard()
    def on_connect(self):

        ChatManager.connect_user_socket(request.user_id, request.sid)
        
        return True
    
    @ConnectionManager.socket_guard()
    def on_join_chat(self, body) :
        ChatManager.join_private_room(request.user_id, body["user_id"], request.sid)

    @ConnectionManager.socket_guard()
    def on_leave_chat(self, body) :
        ChatManager.leave_private_room(request.user_id, body["user_id"], request.sid)

    @ConnectionManager.socket_guard()
    def on_send_message(self, user_message):
        try :
            sender = request.user_id
            receiver = user_message.get("user_id")
            text = user_message.get("text", "").strip()

            if not receiver:
                return False
            
            if not text or len(text) > 1000:
                return False

            return ChatManager.broadcast_message(sender=sender, receiver=receiver, message=text, socket_id=request.sid)
        except Exception as e :
            return False
        
    @ConnectionManager.socket_guard()
    def on_video_call(self,  body):
        if request.user_id == body["user_id"] :
            return
        ChatManager.join_call(request.user_id, body, request.sid)

    @ConnectionManager.socket_guard()
    def on_number_of_messages(self) :
        try :
            out = ChatManager.get_number_of_messages(request.user_id)[0]
            return out
        except Exception as _:
            return 0

    @ConnectionManager.socket_guard()
    def on_disconnect(self, reason):
        ChatManager.disconnect_user_socket(request.user_id, request.sid)
        return