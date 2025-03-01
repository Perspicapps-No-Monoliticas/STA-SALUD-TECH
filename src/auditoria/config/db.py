from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

db = None

DB_USERNAME = os.getenv('DB_USERNAME', default="ingestion")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="admin")
DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")
DB_PORT = os.getenv('DB_PORT', default="5432")
DB_NAME = os.getenv('DB_PORT', default="postgres_auditoria_db")

class DatabaseConfigException(Exception):
    def __init__(self, message='Configuration file is Null or malformed'):
        self.message = message
        super().__init__(self.message)


def database_connection(config, basedir=os.path.abspath(os.path.dirname(__file__))) -> str:
    if not isinstance(config,dict):
        raise DatabaseConfigException
    
    if config.get('TESTING', False) == True:
        return f'sqlite:///{os.path.join(basedir, "database.db")}'
    else:        
        return (f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}:{DB_PORT}/{DB_NAME}")


def init_db(app: Flask):
    global db 
    db = SQLAlchemy(app)