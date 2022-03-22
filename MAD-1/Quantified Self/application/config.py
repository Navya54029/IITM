import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "quantified_self1.sqlite3")
    DEBUG = True
    # SECRET_KEY =  "ash ah secret"
    # SECURITY_REGISTERABLE = True
    # SECURITY_CONFIRMABLE = False
    # SECURITY_SEND_REGISTER_EMAIL = False
    # SECURITY_UNAUTHORIZED_VIEW = None
