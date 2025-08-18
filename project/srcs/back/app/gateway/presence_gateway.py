from flask_socketio import Namespace
from flask import request

class PresenceGateway(Namespace):
    def on_connect(self):
        print ("Hello World", flush=True)
    
    def error_handler(e):
        print ("Hello error", flush=True)
        print (e, flush=True)


    def on_disconnect(self, reason):
        print ("Hello end", flush=True)
        print (reason, flush=True)
