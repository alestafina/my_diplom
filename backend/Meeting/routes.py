from flask import render_template, redirect, url_for, request, flash, session, current_app
from flask_login import login_user, login_required, logout_user
import requests
import json

from Meeting import app, db
from Meeting.models import *

def add_user(Users, role):
    session['id'] = Users.id
    session['name'] = Users.name
    session['email'] = Users.email
    session['role'] = role
    return session

def user_to_db(headers):
    try:
        url_st_info = 'https://api.ciu.nstu.ru/v1.1/student/get_data/app/get_student_info'
        req = requests.get(url_st_info, headers=headers, cookies=session.get('cookies'))
        json_response = req.json()
        information = json_response[0]
        username = information['SURNAME'] + ' ' + information['NAME'] + ' ' + information['PATRONYMIC']
        email = information['EMAIL']
        role = ""
        if information['ROLE'] == 0: 
            new_user = Users(id = information['ID'], name=username, corp_email=email)
            role = "Student"
        else:
            new_user = Users(id = information['ID'], name=username, corp_email=email)
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

def get_teacher_id(_fio, _department):
    t_id = 0

    t_id_query = db.session.query(
    Teachers.teacher_id).join(
    Departments, Teachers.department_id == Departments.department_id).join(
    Users, Teachers.teacher_id == Users.id).filter(
    Users.name == _fio, Departments.short_name == _department)

    t_id = t_id_query.scalar()
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
    # print(json.dumps(data, indent=4, ensure_ascii=False))
    return t_id

def get_group_id(group):
    g_id = 0
    student_group = Students_groups.query.filter_by(name=group).first()
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
    date = datetime.datetime.today()
    # Если сегодня суббота, пропускаем воскресенье
    if date.weekday() == 5:
        date += datetime.timedelta(days=2)
    else:
        date += datetime.timedelta(days=1)
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
            date += datetime.timedelta(days=2)
        else:
            date += datetime.timedelta(days=1)
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
    week_api = 'https://api.ciu.nstu.ru/v1.1/student/get_data/app/get_week_number'
    req = requests.get(week_api, cookies=session.get('cookies'), headers=headers)
    response = req.json()
    cur_week_num = response[0]["WEEK"]
    date = datetime.datetime.today()
    # Если сегодня суббота, пропускаем воскресенье, меняем номер текущей недели
    if date.weekday() == 5:
        date += datetime.timedelta(days=2)
        cur_week_num += 1
    else:
        date += datetime.timedelta(days=1)    
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
            date += datetime.timedelta(days=2)
            cur_week_num += 1
        else:
            date += datetime.timedelta(days=1)
    return result


@app.route("/new_meeting", methods=['GET', 'POST'])
def new_meeting():
    if request.method == 'POST':
        fios = request.form.getlist('name')
        groups = request.form.getlist('group')
        departments = request.form.getlist('department')
        
        for fio, group, department in zip(fios, groups, departments):
            if group:
                group_id = get_group_id(group)
                print(group_id)
                # make_student_schedule(group_id)
            elif department:
                teacher_id = get_teacher_id(fio, department)
                print(teacher_id)
            else:
                flash('Wrong')      
        return "Данные успешно получены!"
    return render_template('new_comand.html')

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login_nstu():
    email = request.form.get('email')
    password = request.form.get('password')

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
            if req.json()['login']:
                user = Users.query.filter_by(corp_email=email).first()
                if user == None:
                    user = user_to_db(headers)
                login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('new_meeting'))
        except Exception as _ex:
            print(_ex)
            flash('Неверно указаны почта или пароль!')
        finally:
            print('ok')
    return render_template('login.html')

