import requests
import json
import psycopg2

from Meeting import db, app
from Meeting.models import *


# url_auth = 'https://api.ciu.nstu.ru/v1.1/token/auth'

# headers = {
#             'Content-Type': 'application/json;charset=utf-8', 
#             'X-OpenAM-Username': login,
#             'X-OpenAM-Password': password,
#             'X-Apikey' : apikey
#         }

# def auth():
#     req = requests.get(url_auth, headers=headers)
#     _cookies = req.cookies
#     print(req)
#     return _cookies

# cookies = auth()
# url = 'https://api.ciu.nstu.ru/v1.1/student/get_data/proj/chairs'

# request = requests.get(url, cookies=cookies, headers=headers)
# response = request.json()

# with open("dep.json", "w") as file:
#     json.dump(response, file, indent=4, ensure_ascii=False)

# -----------------------------
# РАБОЧАЯ ФИГНЯ "ДОБАВИТЬ В БД"
# -----------------------------
# connection = psycopg2.connect(
#         host="localhost",
#         user="admin",
#         password="alestafina",
#         database="db_meeting"
#     )
# connection.autocommit = True
# with connection.cursor() as cursor:
#     with open("dep.json", "r") as file:
#         deps = json.load(file)
#         sql_query = ''
#         for dep in deps:
#             depssql = f"INSERT INTO departments VALUES ({dep['ID']}, {dep['FACULTTY_ID']}, \'{dep['NAME']}\', \'{dep['SNAME']}\');"
#             sql_query += depssql
#         sql_query += 'INSERT INTO departments VALUES (22260, 5, \'Образовательный центр "Центр студенческой проектной деятельности"\', \'ОЦ ЦСПД\')'
        # cursor.execute(sql_query)

