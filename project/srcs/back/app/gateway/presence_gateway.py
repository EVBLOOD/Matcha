from flask_socketio import Namespace
from flask import request
from app.gateway.connection_manager import ConnectionManager
from flask_socketio import disconnect, emit
import json

class PresenceGateway(Namespace):
    @ConnectionManager.socket_guard()
    def on_connect(self):
        ConnectionManager.connect_user(user_id=request.user_id, sid=str(request.sid))
        print (f"Hello World PresenceGateway( on_connect ) {request.user_id}", flush=True)
        return True


    @ConnectionManager.socket_guard()
    def on_check_user_connect(self, id):
        try :
            online = ConnectionManager.is_user_online(int(id))
            # here check friendship status!
            print(f"user {id} : {online}", flush=True)
            return {"status": online}
        except Exception as _:
            return False



    @ConnectionManager.socket_guard()
    def on_check_users_connect(self, ids):
        print(ids, flush=True)
        try :
            status = []
            for id in ids["users"] :
                # here check friendship status!
                online = ConnectionManager.is_user_online(int(id))
                # here I should join the user channel:
                status.append({id: online})
            return status
        except Exception as _:
            return False

    @ConnectionManager.socket_guard()
    def on_like(self, id):
        print(id, flush=True)
        try :
            online = ConnectionManager.is_user_online(int(id))
        except Exception as _:
            return False


    def error_handler(e):
        print ("Hello error", flush=True)
        print (e, flush=True)
        disconnect()


    @ConnectionManager.socket_guard()
    def on_disconnect(self, reason):
        print(f"End call - Reason: {reason}", flush=True)
        ConnectionManager.disconnect_user(sid=request.sid)
        
