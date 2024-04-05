import os

class Config:
    # DATABASE_HOST = 'localhost'
    # DATABASE_NAME = 'db_meeting'
    # DATABASE_USER = 'alestafina'
    # DATABASE_PASSWORD = 'alestafina' 
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'M3jrJplbKp44MTFUhqW9fZtCab3jOJx8'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://admin:alestafina@localhost/db_meeting'
    SQLALCHEMY_TRACK_MODIFICATIONS = False