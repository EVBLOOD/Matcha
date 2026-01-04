import os
from dotenv import load_dotenv
from flask_marshmallow import Marshmallow

load_dotenv ()

class Config:
    DB_HOST = os.getenv('DB_HOST', 'database')
    DB_USER = os.getenv('POSTGRES_USER', 'postgres')
    DB_NAME = os.getenv('POSTGRES_DB', 'matcha')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'No_PASS')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_instence = None
    redis_instence = None
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    JWT_TOKEN_LOCATION = ["headers"]
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    ALLOWED_EXTENSIONS = ""
    UPLOAD_FOLDER = "pictures_storage"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    max_width=5000
    max_height=5000

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT =  int(os.getenv('MAIL_PORT', '587'))
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME =  os.getenv('MAIL_USERNAME', 'noreplay@matcha.com')
    MAIL_PASSWORD =  os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', '')
    FRONT_LINK = os.getenv('FRONT_LINK', 'localhost:300')
    ma_instence = None
    mail = None
    socket_instence = None
