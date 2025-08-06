import os
from dotenv import load_dotenv

load_dotenv ()

class Config:
    DB_HOST = os.getenv('DB_HOST', 'database')
    DB_USER = os.getenv('POSTGRES_USER', 'postgres')
    DB_NAME = os.getenv('POSTGRES_DB', 'matcha')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'No_PASS')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_instence = None
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    JWT_TOKEN_LOCATION = ["headers"]
    # JWT_TOKEN_LOCATION = ["headers", "cookies"]
    # JWT_ACCESS_COOKIE_NAME = "access_token"



