from flask_socketio import Namespace
from flask import request
from app.gateway.connection_manager import ConnectionManager
from app.gateway.chat_manager import ChatManager
from flask_socketio import disconnect, emit
import json

class ChatGateway(Namespace):

    @ConnectionManager.socket_guard()
    def on_connect(self):
        try :
            ChatManager.connect_user_socket(request.user_id, request.sid)
            return True
        except :
            return False
    
    @ConnectionManager.socket_guard()
    def on_join_chat(self, body) :
        try :
            ChatManager.join_private_room(request.user_id, body["user_id"], request.sid)
        except :
            return False

    @ConnectionManager.socket_guard()
    def on_leave_chat(self, body) :
        try :
            ChatManager.leave_private_room(request.user_id, body["user_id"], request.sid)
        except :
            return False

    @ConnectionManager.socket_guard()
    def on_send_message(self, user_message):
        print("con", flush=True)
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
            print(e, flush=True)

            return False
        
    @ConnectionManager.socket_guard()
    def on_video_call(self,  body):
        try :
            if request.user_id == body["user_id"] :
                return
            ChatManager.handle_calls(request.user_id, body, request.sid)
        except Exception as e:
            print(e, flush=True)
            return False

    @ConnectionManager.socket_guard()
    def on_number_of_messages(self) :
        try :
            out = ChatManager.get_number_of_messages(request.user_id)
            return out
        except Exception as _:
            return 0
        
    @ConnectionManager.socket_guard()
    def on_heartbeat_callers(self) :
        try :
            ChatManager.handle_heartbeat(request.user_id)
            return 1
        except Exception as _:
            return 0

    @ConnectionManager.socket_guard()
    def on_disconnect(self, reason):
        try :
            ChatManager.disconnect_user_socket(request.user_id, request.sid)
            return True
        except :
            return False