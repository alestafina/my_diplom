from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_cors import CORS
from config import Config

app = Flask(__name__) # инициализируем приложение
app.config.from_object(Config) # вписываем наши ланные конфигурации
CORS(app, supports_credentials=True, origins="http://217.71.129.139") # разрешаем серверу отправлять данные, куки на фронт

db = SQLAlchemy(app) # подключаем бд
migrate = Migrate(app, db) # создаем миграции бд

manager = LoginManager() # создаем менеджер логинов 
manager.init_app(app) # обеспечиваем связь менеджера с нашим приложением (входы/выходы app)

mail = Mail(app) # подключение почтовой службы

from Meeting import models, routes
