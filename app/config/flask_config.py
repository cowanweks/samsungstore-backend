import os
import secrets

from cachelib.file import FileSystemCache
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class DBConfig(object):
    """Configs for the database"""

    SQLALCHEMY_DATABASE_URI = (
        os.getenv("SQLALCHEMY_DATABASE_URI") or "sqlite:///ringstech.db"
    )


class Config(DBConfig):
    """Base Application Config"""

    PORT = 3001
    DEBUG = True
    TESTING = False
    HOST = "0.0.0.0"
    WTF_CSRF_ENABLED = False
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASSWD = os.getenv("SMTP_PASSWD")
    BASE_URL = os.getenv("BASE_URL") or "127.0.0.1"

    # Session settings
    SESSION_TYPE = "cachelib"
    SESSION_USE_SIGNER = True
    SESSION_SERIALIZATION_FORMAT = "json"
    SECRET_KEY = secrets.token_hex(16)
    SESSION_CACHELIB = FileSystemCache(threshold=500, cache_dir="sessions")

    APP_NAME = "RingsTech"


class DevelopmentConfig(Config):
    """Config for Development"""

    APP_ENV = "development"
    pass


class TestingConfig(Config):
    """Config for Testing"""

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    APP_ENV = "testing"
    TESTING = True


class ProductionConfig(Config):
    """Config for Production"""

    APP_ENV = "production"
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI =\
        "postgresql://ohvomqcn:zy3VFG-FlCYScCpEyyGRT3xwehbvZ-Au@suleiman.db.elephantsql.com/ohvomqcn"
