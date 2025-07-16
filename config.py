import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://admin:secretpassword@localhost:9000/socialmediadb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
