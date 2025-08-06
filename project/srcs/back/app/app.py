from flask import Flask
from app.routes.user_route import user_bp
from app.routes.auth_route import auth_bp
from app.core.database import Database
from app.core.config import Config
from app.core.security import Security



app = Flask(__name__)
Config.DB_instence = Database(app=app)

app.config.from_object(Config)
Security().init_jwt(app)

app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)

app.run(host="0.0.0.0", port="8080")

