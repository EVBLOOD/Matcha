from flask import Flask

from app.core.database import Database
from app.core.config import Config
from app.core.security import Security
from flask_redis import FlaskRedis
from flask_mail import Mail
from flask_socketio import SocketIO
from app.gateway.presence_gateway import PresenceGateway
from app.gateway.chat_gateway import ChatGateway

from flask_marshmallow import Marshmallow
from flask_cors import CORS

import os
import geoip2.database
from werkzeug.middleware.proxy_fix import ProxyFix
import requests


app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

app.config.from_object(Config)
Config.DB_instence = Database(app=app)
Config.redis_instence = FlaskRedis(app=app)
CORS(app)
Security().init_jwt(app)
Config.mail = Mail(app)

Config.ma_instence = Marshmallow(app=app)

try :
    Config.GEOIP_READER = geoip2.database.Reader(Config.GEOIP_DB_PATH)
except Exception as e:
    print(f"Please verify you env vars! or {e}", flush=True)


try:
    response = requests.get("https://1.1.1.1/cdn-cgi/trace")
    for line in response.text.split('\n'):
        if line.startswith('ip=') :
            Config.PUBLIC_IP = line.split('=')[1]
except Exception:
    Config.PUBLIC_IP = "8.8.8.8"

print(f"Config->PUBLIC_IP: {Config.PUBLIC_IP}", flush=True)

Config.socket_instence = SocketIO(app, cors_allowed_origins="*",resource_path='/socket.io')
Config.socket_instence.on_namespace(PresenceGateway('/status'))
Config.socket_instence.on_namespace(ChatGateway('/chat'))

from app.controllers.user_route import user_bp
from app.controllers.auth_route import auth_bp
from app.controllers.profile_route import profile_bp
from app.controllers.notifs_route import notifs_bp
from app.controllers.chats_route import chats_bp
from app.controllers.suggestions_route import suggestions_bp
from app.controllers.inteructions_route import inteructions_bp
from app.controllers.dates_route import dates_bp

app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(notifs_bp)
app.register_blueprint(chats_bp)
app.register_blueprint(suggestions_bp)
app.register_blueprint(inteructions_bp)

app.register_blueprint(dates_bp)

# Config.socket_instence.run(app, host="0.0.0.0", port=8080)

