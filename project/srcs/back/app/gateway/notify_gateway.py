from flask_socketio import Namespace
from flask import request
from app.gateway.connection_manager import ConnectionManager
from flask_socketio import disconnect, emit
import json

class NotifyGateway(Namespace):
    @ConnectionManager.socket_guard()
    def on_connect(self):
        ConnectionManager.connect_user(user_id=request.user_id, sid=str(request.sid))
        return True

    
    def error_handler(e):
        disconnect()

    # def on_message(self, user_message) :
    #     user


    @ConnectionManager.socket_guard()
    def on_disconnect(self, reason):
        if request.sid:
            ConnectionManager.disconnect_user(sid=request.sid)
        return
        
