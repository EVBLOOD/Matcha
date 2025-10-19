from flask_socketio import Namespace
from flask import request
from app.gateway.connection_manager import ConnectionManager
from flask_socketio import disconnect, emit
import json

class PresenceGateway(Namespace):
    @ConnectionManager.socket_guard()
    def on_connect(self):
        ConnectionManager.connect_user(user_id=request.user_id, sid=str(request.sid))
        print (f"Hello World {request.user_id}", flush=True)
        return True

    
    def error_handler(e):
        print ("Hello error", flush=True)
        print (e, flush=True)
        disconnect()


    @ConnectionManager.socket_guard()
    def on_disconnect(self, reason):
        print(f"End call - Reason: {reason}", flush=True)
        if request.sid:
            ConnectionManager.disconnect_user(sid=request.sid)
        return
        
