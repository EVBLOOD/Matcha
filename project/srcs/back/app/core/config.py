import os
from dotenv import load_dotenv

load_dotenv ()

class Config:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('POSTGRES_USER', 'postgres')
    DB_NAME = os.getenv('POSTGRES_DB', 'matcha')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', '')
    DB_PORT = os.getenv('DB_PORT', '5432')