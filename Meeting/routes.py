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
        url_info = 'https://api.ciu.nstu.ru/v1.1/student/get_data/app/get_student_info'
        req = requests.get(url_info, headers=headers, cookies=session.get('cookies'))
        json_response = req.json()
        information = json_response[0]
        username = information['SURNAME'] + ' ' + information['NAME'] + ' ' + information['PATRONYMIC']
        email = information['EMAIL']
        role = ""
        if information['ROLE'] == 0: # Проверять работающих студентов 
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
            new_teacher = Teachers(teacher_id=new_user.id, faculty_id = information['ID_FACULTET'])
            db.session.add(new_teacher)
            db.session.commit()
    except Exception as _ex:
        print(_ex)
    finally:
        return new_user


@app.route("/")
@app.route("/index", methods=['GET'])
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
                return redirect(url_for('index'))
        except Exception as _ex:
            print(_ex)
            flash('Неверно указаны почта или пароль!')
        finally:
            print('ok')

    return render_template('login.html')
