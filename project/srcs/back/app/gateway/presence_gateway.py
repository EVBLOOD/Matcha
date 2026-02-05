from flask_socketio import Namespace
from flask import request
from app.gateway.connection_manager import ConnectionManager
from flask_socketio import disconnect, emit
import json

# from app.services.dates_service import DatesService


class PresenceGateway(Namespace):
    @ConnectionManager.socket_guard()
    def on_connect(self):
        try :
            ConnectionManager.connect_user(user_id=request.user_id, sid=str(request.sid))
            return True
        except :
            return False

    @ConnectionManager.socket_guard()
    def on_ping(self):
        ConnectionManager.heartbeat(request.user_id)

    @ConnectionManager.socket_guard()
    def on_check_user_connect(self, id):
        try :
            online = ConnectionManager.is_user_online(int(id), request.user_id)
            return {"status": online}
        except Exception as _:
            return False



    @ConnectionManager.socket_guard()
    def on_check_users_connect(self, ids):
        try :
            status = []
            for id in ids["users"] :
                # here check friendship status!
                online = ConnectionManager.is_user_online(int(id), request.user_id)
                # here I should join the user channel:
                status.append({id: online})
            return status
        except Exception as _:
            return False

    @ConnectionManager.socket_guard()
    def on_like(self, id):
        try :
            ConnectionManager.interact_with_user(request.user_id, int(id), "Like")
        except Exception as _:
            print("Hello wold !", flush=True)
            return False

    @ConnectionManager.socket_guard()
    def on_dislike(self, id):
        try :
            ConnectionManager.interact_with_user(request.user_id, int(id), "Dislike")
        except Exception as _:
            return False

    @ConnectionManager.socket_guard()
    def on_view(self, id):
        try :
            print("LOLO", flush=True)
            ConnectionManager.interact_with_user(request.user_id, int(id), "View")
        except Exception as _:
            return False

    @ConnectionManager.socket_guard()
    def on_block(self, id):
        try :
            ConnectionManager.interact_with_user(request.user_id, int(id), "Block")
        except Exception as _:
            return False

    @ConnectionManager.socket_guard()
    def on_unblock(self, id):
        try :
            ConnectionManager.interact_with_user(request.user_id, int(id), "Unblock")
        except Exception as _:
            return False

    @ConnectionManager.socket_guard()
    def on_propose_date(self, body):
        try :
            date_id = ConnectionManager.propose_date(request.user_id, body)
            return date_id
        except Exception as e :
            print (e, flush=True)
            return False


    @ConnectionManager.socket_guard()
    def on_respond_to_date(self, body):
        try :            
            ConnectionManager.respond_to_date(request.user_id, body)
            return True
        except Exception as e :
            print (e, flush=True)
            return False

    def error_handler(e):
        disconnect()

    @ConnectionManager.socket_guard()
    def on_number_of_notifs(self) :
        try :
            out = ConnectionManager.get_number_of_notifs(request.user_id)
            print(out, flush=True)
            return out
        except Exception as _:
            return 0


    # @ConnectionManager.socket_guard()
    def on_disconnect(self, reason):
        try :
            print(f"End call - Reason: {reason}", flush=True)
            ConnectionManager.disconnect_user(sid=request.sid)
        except Exception as e:
            print(f"exception is hole {e}", flush=True)
            return False
        
