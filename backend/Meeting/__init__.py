from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from flask_cors import CORS

app = Flask(__name__) # инициализируем приложение
CORS(app, supports_credentials=True) # разрешаем серверу отправлять данные, куки на фронт
app.config.from_object(Config) # вписываем наши ланные конфигурации
db = SQLAlchemy(app) # подключаем бд
migrate = Migrate(app, db) # создаем миграции бд
manager = LoginManager() # создаем менеджер логинов 
manager.init_app(app) # обеспечиваем связь менеджера с нашим приложением (входы/выходы app)

from Meeting import models, routes
