from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from db_config import Config

app = Flask(__name__)
app.config.from_object('db_config.Config')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://alestafina:alestafina@localhost/db_meeting'
db = SQLAlchemy(app)
manager = LoginManager()
manager.init_app(app)

from Meeting import routes
