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


app = Flask(__name__)
app.config.from_object(Config)
Config.DB_instence = Database(app=app)
Config.redis_instence = FlaskRedis(app=app)

Security().init_jwt(app)
Config.mail = Mail(app)

Config.ma_instence = Marshmallow(app=app)


Config.socket_instence = SocketIO(app, cors_allowed_origins="*")
Config.socket_instence.on_namespace(PresenceGateway('/status'))
Config.socket_instence.on_namespace(ChatGateway('/chat'))

from app.controllers.user_route import user_bp
from app.controllers.auth_route import auth_bp
from app.controllers.profile_route import profile_bp

app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(profile_bp)

# Config.socket_instence.run(app, host="0.0.0.0", port=8080)

