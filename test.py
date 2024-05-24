import requests
import json
import datetime as dt

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

def auth():
    req = requests.get(url_auth, headers=headers)
    _cookies = req.cookies
    print(req)
    return _cookies

# формируем объект с расписанием преподавателя
def make_teacher_schedule(teacher_id):
    # получаем расписание преподавателя
    url_get_teacher = f'https://api.ciu.nstu.ru/v1.1/student/get_data/app/get_teacher_schedule/{teacher_id}'
    req = requests.get(url_get_teacher, cookies=cookies, headers=headers)
    data = req.json()
    # формируем формат для будущего поиска
    result = {"name": data[0]["TEACHER_FIO"], "days": []}
    date = dt.datetime.today()
    # Если сегодня суббота, пропускаем воскресенье
    if date.weekday() == 5:
        date += dt.timedelta(days=2)
    else:
        date += dt.timedelta(days=1)
    # 12 дней (2 недели без воскресений)
    for i in range(1, 13):
        lessons = {f"lesson {j}": 1 for j in range(1, 8)}
        date_str = date.isoformat().split("T")[0]
        for item in data:
            date_in_tt = item["DAY_DATE"].split("T")[0]
            if date_str == date_in_tt:
                lessons[f"lesson {item['POSITION']}"] = 0  # Устанавливаем 1 для найденного урока
        result["days"].append({"date": date_str, f"day {i}": lessons})
        # Если суббота, пропускаем воскресенье
        if date.weekday() == 5:
            date += dt.timedelta(days=2)
        else:
            date += dt.timedelta(days=1)
    return result

# формируем объект с расписанием студента
def make_student_schedule(student_id):
    # получаем расписание студента
    url_get_student = f'https://api.ciu.nstu.ru/v1.1/student/get_data/app/get_student_schedule/{student_id}'
    req = requests.get(url_get_student, cookies=cookies, headers=headers)
    data = req.json()
    # формируем формат для поиска 
    result  = {"name": data[0]['STUDY_GROUP'], "days": []}
    weeks = [] 
    # получаем номер текущей недели
    week_api = 'https://api.ciu.nstu.ru/v1.1/student/get_data/app/get_week_number'
    req = requests.get(week_api, cookies=cookies, headers=headers)
    response = req.json()
    cur_week_num = response[0]["WEEK"]
    date = dt.datetime.today()
    # Если сегодня суббота, пропускаем воскресенье, меняем номер текущей недели
    if date.weekday() == 5:
        date += dt.timedelta(days=2)
        cur_week_num += 1
    else:
        date += dt.timedelta(days=1)    
    for i in range(1, 13):
        lessons = {f"lesson {j}": 1 for j in range(1, 8)}
        date_str = date.isoformat().split("T")[0]
        day_week = date.weekday() + 1
        for item in data:
            if item['WEEK'] != None:
                weeks = [int(num) for num in item['WEEK'].split(",")]
            if item['DAY_NUMBER'] == day_week:
                if item['WEEK'] == None:
                    if item['FREQUENCY'] == 1 and cur_week_num % 2 == 0: # четная неделя
                        lessons[f"lesson {item['POSITION']}"] = 0  
                    elif item['FREQUENCY'] == 2 and cur_week_num % 2 != 0: # нечетная неделя
                        lessons[f"lesson {item['POSITION']}"] = 0 
                    elif item['FREQUENCY'] == 3: # любая неделя
                        lessons[f"lesson {item['POSITION']}"] = 0
                elif cur_week_num in weeks: # FREQUENCY=7, особые номера недель
                    lessons[f"lesson {item['POSITION']}"] = 0  
        result["days"].append({"date": date_str, f"day {i}": lessons})     
        # Если суббота, пропускаем воскресенье, меняем номер текущей недели
        if date.weekday() == 5:
            date += dt.timedelta(days=2)
            cur_week_num += 1
        else:
            date += dt.timedelta(days=1)
    return result

# ДА ВОЗМОЖНО ЭТО ГРОМОЗДКО И КАЖЕТСЯ ЧТО У МЕНЯ ОЧЕНЬ ТУПАЯ СТРУКТУРА В ЛОБ
# но я ничего другого не придумала
# функция поиска свободных окон
def search_free(schedule):
    free_time = schedule[0]
    free_time.pop("name")
    # Для каждого человека
    for i in range(len(schedule)):
        # Для каждого дня
        for day in range(1, 13):
            # Для каждой пары
            for j in range(1, 8):
                free_time["days"][day - 1][f"day {day}"][f"lesson {j}"] *= schedule[i]["days"][day - 1][f"day {day}"][f"lesson {j}"]
    return free_time

cookies = auth()
schedule = []

teacher_id = 21874
student_id = 68719

res = make_teacher_schedule(teacher_id)
schedule.append(res)
res = make_student_schedule(student_id)
schedule.append(res)

free = search_free(schedule)

with open("free.json", "w") as out:
    json.dump(free, out, indent=4, ensure_ascii=False)

# def dates():
#     date = dt.datetime.today()
#     dates = []
#     # Если сегодня суббота, пропускаем воскресенье, меняем номер текущей недели
#     for i in range(0,12):
#         if date.weekday() == 5:
#             date += dt.timedelta(days=2)
#         else:
#             date += dt.timedelta(days=1)
#         date_str = date.isoformat().split("T")[0]
#         dates.append(date_str)
#     print(dates)
#     return dates

# dates()
