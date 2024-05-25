import os

class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'M3jrJplbKp44MTFUhqW9fZtCab3jOJx8'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://admin:alestafina@localhost/db_meeting'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.mail.ru'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'meeting_app@mail.ru'
    MAIL_PASSWORD = 'hqimk8i42e6YVQUqixYr'
    MAIL_DEFAULT_SENDER = 'meeting_app@mail.ru'

