import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    SECRET_KEY = "abiughweiofhweofijhwerkhwef"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET_KEY = os.getenv("GOOGLE_CLIENT_SECRET_KEY")

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///books.db'
    DEBUG = True

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    DEBUG = False

