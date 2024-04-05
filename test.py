import requests

login = 'mustafina.2020@stud.nstu.ru'
password = 'Astro24105804'
apikey = 'FB8EEED25F6150E3E0530718000A3425'

url_auth = 'https://api.ciu.nstu.ru/v1.1/token/auth'

headers = {
            'Content-Type': 'application/json;charset=utf-8', 
            'X-OpenAM-Username': login,
            'X-OpenAM-Password': password,
            'X-Apikey' : apikey
        }

req = requests.get(url_auth, headers=headers)
cookies = req.cookies
print(req)

url_get_teacher = 'https://api.ciu.nstu.ru/v1.1/student/get_data/app/get_teacher_schedule/827'
url_get_student = 'https://api.ciu.nstu.ru/v1.1/student/get_data/app/get_student_schedule/36535'
url_get_room = 'https://api.ciu.nstu.ru/v1.1/student/get_data/app/get_room_schedule/475'

req = requests.get(url_get_teacher, cookies=cookies, headers=headers)
response = req.json()

print(response[1]['DISCIPLINE_NAME'])