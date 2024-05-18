from flask import request, session
from flask_login import login_user, login_required, logout_user, current_user
import requests
import datetime as dt
import locale
from flask import jsonify

from Meeting import app, db, manager
from Meeting.models import *

# добавляем нужную информацию о юзере в сессию
def add_user(Users, role):
    session['id'] = Users.id
    session['name'] = Users.name
    session['email'] = Users.corp_email
    session['role'] = role
    return session

# если юзера нет в бд, добавляем, выхватывая данные из ИС
def user_to_db(headers, email):
    try:
        url_st_info = 'https://api.ciu.nstu.ru/v1.1/student/get_data/app/get_student_info'
        req = requests.get(url_st_info, headers=headers, cookies=session.get('cookies'))
        json_response = req.json()
        information = json_response[0]
        username = information['SURNAME'] + ' ' + information['NAME'] + ' ' + information['PATRONYMIC']
        role = ""
        new_user = Users(id = information['ID'], name=username, corp_email=email)
        if information['ROLE'] == 0: 
            role = "Student"
        else:
            role = "Teacher"
        db.session.add(new_user)
        db.session.commit()
        new_user = Users.query.filter_by(corp_email=email).first()
        if role == "Student":
            group = Students_groups.query.filter_by(group_id=information['ID_GROUP']).first()
            if group == None:
                group = Students_groups(group_id = information['ID_GROUP'], faculty_id=information['ID_FACULTET'], name=information['SYM_GROUP'])
                db.session.add(group)
                db.session.commit()
                group = Students_groups.query.filter_by(group_id=information['ID_GROUP']).first()
            student = Students(student_id = new_user.id, group_id = group.group_id)
            db.session.add(student)
            db.session.commit()
        elif role == "Teacher":
            # для преподавателя, чтоб узнат кафедру ищем его в ИС
            url_t_id = 'https://api.ciu.nstu.ru/v1.1/student/get_data/proj/teachers'
            req_t = requests.get(url_t_id, headers=headers, cookies=session.get('cookies'))
            teachers = req_t.json()
            for teacher in teachers:
                if teacher['IDPERSON'] == new_user.id:
                    department_id = teacher['CHAIR_ID']
                    break
            new_teacher = Teachers(teacher_id=new_user.id, department_id = department_id)
            db.session.add(new_teacher)
            db.session.commit()
    except Exception as _ex:
        print(_ex)
    finally:
        return new_user

# создаем расписание для авторизированного пользователя
def make_my_schedule():
    schedule = {}
    if session.get('role') == 'Student':
        student = Students.query.filter_by(student_id=session.get('id')).first()
        group_id = student.group_id
        schedule = make_student_schedule(group_id)
    else:
        schedule = make_teacher_schedule(session.get('id'))
    return schedule

# получаем айди преподавателя из бд или ИС если такого нет
def get_teacher_id(_fio, _department):
    # большой запрос на поиск препода
    t_id_query = db.session.query(
    Teachers.teacher_id).join(
    Departments, Teachers.department_id == Departments.department_id).join(
    Users, Teachers.teacher_id == Users.id).filter(
    Users.name == _fio, Departments.short_name == _department)

    t_id = t_id_query.scalar()
    # не нашли препода - ищем в ИС и добавляем в бд
    if t_id == None:
        url_get_teachers = 'https://api.ciu.nstu.ru/v1.1/student/get_data/proj/teachers'
        headers = {
            'Content-Type': 'application/json;charset=utf-8',
            'X-Apikey': 'FB8EEED25F6150E3E0530718000A3425'
        }
        req = requests.get(url_get_teachers, cookies=session.get('cookies'), headers=headers)
        data = req.json()
        fio_as_list = _fio.split()
        dep = Departments.query.filter_by(short_name=_department).first()
        dep_id = dep.department_id
        for teacher in data:
            if fio_as_list[0] == teacher.get('SURNAME') and\
            fio_as_list[1] == teacher.get('NAME')       and\
            fio_as_list[2] == teacher.get('PATRONYMIC') and\
            teacher.get('CHAIR_ID') == dep_id:
                t_id = teacher.get('IDPERSON')
        url_get_t_info = f'https://api.ciu.nstu.ru/v1.1/student/get_data/app/get_teacher_info/{t_id}'
        req_t = requests.get(url_get_t_info, headers=headers, cookies=session.get('cookies'))
        t_info = req_t.json()[0]
        new_teacher = Users(id=t_info['ID'], name=t_info['FULL_FIO'], corp_email=t_info['EMAIL'])
        db.session.add(new_teacher)
        db.session.commit()
        t_in_t = Teachers(teacher_id=t_id, department_id=dep_id)
        db.session.add(t_in_t)
        db.session.commit()
    return t_id

# ищем айди группы студента
def get_group_id(group):
    student_group = Students_groups.query.filter_by(name=group).first()
    # если не нашли в бд, ищем в ИС - добавляем в бд
    if student_group == None:
        url_get_groups = 'https://api.ciu.nstu.ru/v1.1/student/get_data/proj/groups'
        headers = {
            'Content-Type': 'application/json;charset=utf-8',
            'X-Apikey': 'FB8EEED25F6150E3E0530718000A3425'
        }
        req = requests.get(url_get_groups, cookies=session.get('cookies'), headers=headers)
        data = req.json()
        for groups in data:
            if groups.get('NAME') == group:
                info = groups
                break
        student_group = Students_groups(group_id = info.get('ID'), faculty_id=info.get('ID_FACULTET'), name=info.get('NAME'))
        db.session.add(student_group)
        db.session.commit()
    g_id = student_group.group_id
    return g_id

def make_teacher_schedule(teacher_id):
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'X-Apikey': 'FB8EEED25F6150E3E0530718000A3425'
    }
    # получаем расписание преподавателя
    url_get_teacher = f'https://api.ciu.nstu.ru/v1.1/student/get_data/app/get_teacher_schedule/{teacher_id}'
    req = requests.get(url_get_teacher, cookies=session.get('cookies'), headers=headers)
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
                lessons[f"lesson {item['POSITION']}"] = 0  
        result["days"].append({"date": date_str, f"day {i}": lessons})
        # Если суббота, пропускаем воскресенье
        if date.weekday() == 5:
            date += dt.timedelta(days=2)
        else:
            date += dt.timedelta(days=1)
    return result

def make_student_schedule(group_id):
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'X-Apikey': 'FB8EEED25F6150E3E0530718000A3425'
    }
    # получаем расписание студента
    url_get_student = f'https://api.ciu.nstu.ru/v1.1/student/get_data/app/get_student_schedule/{group_id}'
    req = requests.get(url_get_student, cookies=session.get('cookies'), headers=headers)
    data = req.json()
    # формируем формат для поиска 
    result  = {"name": data[0]['STUDY_GROUP'], "days": []}
    weeks = [] 
    # получаем номер текущей недели
    cur_week_num = week_now()
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
                    # четная неделя
                    if item['FREQUENCY'] == 1 and cur_week_num % 2 == 0: 
                        lessons[f"lesson {item['POSITION']}"] = 0
                    # нечетная неделя
                    elif item['FREQUENCY'] == 2 and cur_week_num % 2 != 0: 
                        lessons[f"lesson {item['POSITION']}"] = 0 
                    # любая неделя
                    elif item['FREQUENCY'] == 3: 
                        lessons[f"lesson {item['POSITION']}"] = 0
                # FREQUENCY=7, особые номера недель
                elif cur_week_num in weeks: 
                    lessons[f"lesson {item['POSITION']}"] = 0  
        result["days"].append({"date": date_str, f"day {i}": lessons})     
        # Если суббота, пропускаем воскресенье, меняем номер текущей недели
        if date.weekday() == 5:
            date += dt.timedelta(days=2)
            cur_week_num += 1
        else:
            date += dt.timedelta(days=1)
    return result

def week_now():
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'X-Apikey': 'FB8EEED25F6150E3E0530718000A3425'
    }
    week_api = 'https://api.ciu.nstu.ru/v1.1/student/get_data/app/get_week_number'
    req = requests.get(week_api, cookies=session.get('cookies'), headers=headers)
    response = req.json()
    return response[0]["WEEK"]

# обнуляем окна, соотевствующие уже существующим встречам (берем из бд)
def make_meeting_schedule(schedule):
    result = schedule
    member = db.session.query(Meeting_members).filter_by(user_id=session['id']).all()
    for i in member:
        meeting = Meeting.query.filter_by(meeting_id=i.meeting_id).first()
        for day in range(1,13):
            if result["days"][day - 1]["date"] == meeting.date.strftime('%Y-%m-%d'):
                result["days"][day - 1][f"day {day}"][f"lesson {meeting.lesson_id}"] = 0 
    return result

def remove_time_with_meet(fio, role, _id, schedule):
    try:
        if role == 'student':
            student = Students.query.join(Users).filter(
                Users.name == fio, Users.id == Students.student_id, Students.group_id == _id).first()
            user_id = student.student_id 
        else: 
            user_id = _id
        member = db.session.query(Meeting_members).filter_by(user_id=user_id).all()
        for idf in member:
            meeting = Meeting.query.filter_by(meeting_id=idf.meeting_id).first()
            for day in range(1,13):
                if schedule["days"][day - 1]["date"] == meeting.date.strftime('%Y-%m-%d'):
                    schedule["days"][day - 1][f"day {day}"][f"lesson {meeting.lesson_id}"] = 0 
    except Exception as _ex:
        print(_ex)

# ищем свободные окна для всех
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

# добавляем команду в бд
def add_team(data):
    try:
        team = Team.query.filter_by(title=data.get('title'), lead_user_id=session['id']).first()
        if team:
            return 0
        else:
            team = Team(title=data.get('title'), lead_user_id=session['id'])
            db.session.add(team)
            db.session.commit()
            return team.team_id
    except Exception as _ex:
        print(_ex)

def add_team_member(fio, role, _id, title):
    try:
        if role == 'student':
            team = Team.query.filter_by(title=title, lead_user_id=session['id']).first()
            student = Students.query.join(Users).filter(
                Users.name == fio, Users.id == Students.student_id, Students.group_id == _id).first()
            team_member = Team_members(team_id=team.team_id, user_id=student.student_id)
        else: 
            team = Team.query.filter_by(title=title, lead_user_id=session['id']).first()
            team_member = Team_members(team_id=team.team_id, user_id=_id)
        db.session.add(team_member)
        db.session.commit()
    except Exception as _ex:
        print(_ex)

# форматированные даты и часы пар для вывода в таблице
def format_data(data):
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    d_m_dates = [datetime.strptime(day['date'], '%Y-%m-%d').strftime('%d.%m.%y') for day in data['days']]
    d_of_week = [datetime.strptime(day['date'], '%Y-%m-%d').strftime('%a') for day in data['days']]
    
    return d_m_dates, d_of_week

@app.route("/teams", methods=['GET', 'POST'])
@login_required
def teams():
    try:
        teams = db.session.query(Team).filter_by(lead_user_id=session['id']).all()
        if teams == []:
            return jsonify({'massage': 'Вы пока не создали ни одной команды.'})
        else: 
            teams_list = []
            for team in teams:
                title = team.title
                members = db.session.query(Team_members).filter_by(team_id=team.team_id).all()
                team_members = []
                for member in members:
                    user = Users.query.filter_by(id=member.user_id).first()
                    student = Students.query.filter_by(student_id=member.user_id).first()
                    if student:
                        group = Students_groups.query.filter_by(group_id=student.group_id).first()
                        group_name = group.name
                        member = {'name': user.name, 'group': group_name, 'dep': ''}
                    else:
                        teacher = Teachers.query.filter_by(teacher_id=member.user_id).first()
                        dep = Departments.query.filter_by(department_id=teacher.department_id).first()
                        dep_name = dep.short_name
                        member = {'name': user.name, 'group': '', 'dep': dep_name}
                    team_members.append(member)
                teams_list.append({'title': title, 'members': team_members})
            return jsonify(teams_list)
    except Exception as e:
        print(e)
        jsonify({'error': '123'}), 400
        

# создание списка людей и вывод таблицы 
@app.route("/new_meeting", methods=['GET', 'POST'])
@login_required
def new_meeting():
    try:
        if request.method == 'POST':
            data = request.json
            fios = data.get('name')
            groups = data.get('group')
            departments = data.get('department')
            if data.get('save') and fios:
                team = add_team(data)
                if team == 0:
                    return jsonify({'error': 'Команда с таким названием уже существует.'}), 400
            full_schedule = []
            print(data)
            for fio, group, department in zip(fios, groups, departments):
                if fio != session['name']: 
                    if group:
                        group_id = get_group_id(group)
                        print('OK')
                        if data.get('save'):
                            add_team_member(fio, 'student', group_id, data.get('title'))
                        st_schedule = make_student_schedule(group_id)
                        remove_time_with_meet(fio, 'student', group_id, st_schedule)
                        full_schedule.append(st_schedule)
                    elif department != '':
                        teacher_id = get_teacher_id(fio, department)
                        if data.get('save'):
                            add_team_member(fio, 'teacher', teacher_id, data.get('title'))
                        t_schedule = make_teacher_schedule(teacher_id)
                        remove_time_with_meet(fio, 'teacher', group_id, t_schedule)
                        full_schedule.append(t_schedule)
                elif fio == session['name']:
                    return jsonify({'error': 'Свои данные вводить не нужно.'}), 400
                else:
                    return jsonify({'error': 'Введите участника либо удалите неиспользуемое поле.'}), 400
            if full_schedule:
                full_schedule.append(make_my_schedule())
                free = search_free(full_schedule)
                d_m_date, d_of_week = format_data(free)
                final = make_meeting_schedule(free)
                return jsonify({
                    'schedule': final,
                    'd_m_date': d_m_date,
                    'd_of_week': d_of_week,
                }), 200
    except Exception as e:
        print(e)
        jsonify({'error': 'Проверьте введенные данные. Возможно, некоторых участников вы указали неправильно.'}), 400
    return jsonify({'error': 'Необходим хотя бы один участник.'}), 405

# запись данных о встрече в бд
@app.route("/choice", methods=['GET', 'POST'])
@login_required
def choice():
    try:
        if request.method == 'POST':
            data = request.json
            date_from = datetime.strptime(data.get('date'), "%d.%m.%y").date()
            l_id = Lessons.query.filter_by(time=data.get('time')).first()
            lesson_id = l_id.lesson_id
            meeting = Meeting.query.filter_by(date=date_from, lesson_id=lesson_id).first()
            if meeting:
                return jsonify({'error': 'Эту дату нельзя выбрать, пожалуйста выберете другую.'})
            else:
                meeting = Meeting(theme=data.get('theme'), date=date_from, lesson_id=lesson_id)
                db.session.add(meeting)
                db.session.commit()
                if data.get('type') == 'online':
                    meet_type = Online(online_id=meeting.meeting_id, link_to_chat=data.get('meet'))
                else:
                    meet_type = Offline(offline_id=meeting.meeting_id,place=data.get('meet'))
                db.session.add(meet_type)
                db.session.commit()
                for fio in data.get('names'):
                    member = Users.query.filter_by(name=fio).first()
                    m_id = member.id
                    meet_member = Meeting_members(meeting_id=meeting.meeting_id, user_id=m_id)
                    db.session.add(meet_member)
                    db.session.commit()
                meet_member = Meeting_members(meeting_id=meeting.meeting_id, user_id=session['id'])
                db.session.add(meet_member)
                db.session.commit()
                return jsonify({'massage': 'Данные успешно записаны'}), 200
    except Exception as e:
        print(e)
        jsonify({'error': 'Что-то пошло не так.'}), 400
    return jsonify({'error': 'Ошибка при отправке данных.'}), 400

@app.route("/main", methods=['GET', 'POST'])
@login_required
def main():
    week_number = week_now()
    return jsonify({'week' : week_number})

@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

# Авторизация НГТУ
@app.route("/login", methods=['GET', 'POST'])
def login_nstu():
    if request.method == 'POST':
        data = request.json
        email = data.get('email')
        password = data.get('password')
        if email and password:
            url_auth = 'https://api.ciu.nstu.ru/v1.1/token/auth'
            headers = {
                'Content-Type': 'application/json;charset=utf-8',
                'X-OpenAM-Username': email,
                'X-OpenAM-Password': password
            }
            req = requests.get(url_auth, headers=headers)
            session['cookies'] = dict(req.cookies)
            try:
                if req.status_code == 200 and req.json()['login']:
                    user = Users.query.filter_by(corp_email=email).first()
                    if user == None:
                        user = user_to_db(headers, email)
                    login_user(user)
                    if Teachers.query.filter_by(teacher_id=user.id).first() != None:
                        add_user(user, "Teacher")
                    else:
                        add_user(user, "Student")
                print('auth ' + str(current_user.is_authenticated))
                return jsonify({'massage': 'Классный пароль!'}), 200
            except Exception as e:
                print(e)
                return jsonify({'error': 'Неверно указаны почта или пароль!'}), 400
        else: 
            return jsonify({'error': 'Нет данных'}), 400
    else:
        return jsonify({'massage': 'страница логина'})

@app.route('/checkAuth', methods=['GET'])
def check_auth():
    url_check = 'https://api.ciu.nstu.ru/v1.1/token/show'
    headers = {
        'Content-Type': 'application/json;charset=utf-8'
    }
    req = requests.get(url_check, headers=headers, cookies=session.get('cookies'))
    resp = req.json()
    if resp.get('msg') is None: 
        print('yes! ')
        return jsonify({'isAuth': True}), 200
    else:
        print('no!')
        return jsonify({'isAuth': False}), 200


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    session.pop('cookies', None)
    logout_user()
    return ({'massage': 'Успешный выход!'})
