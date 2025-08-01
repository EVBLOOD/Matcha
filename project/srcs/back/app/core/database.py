from .config import Config

class Database :
    def __init__ (self) :
        db_link = f"postgresql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"
        print (db_link)
      