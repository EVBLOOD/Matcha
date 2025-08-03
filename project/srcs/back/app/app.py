from flask import Flask
from app.routes.user_route import user_bp
from app.core.database import Database
from app.core.config import Config


app = Flask(__name__)

Config.DB_instence = Database(app=app)

app.register_blueprint(user_bp)

app.run(host="0.0.0.0", port="8080")

