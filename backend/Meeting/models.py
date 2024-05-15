from Meeting import db
from flask_login import UserMixin
from datetime import datetime

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    corp_email = db.Column(db.String(128), unique=True)

class Faculties(db.Model):
    faculty_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(128), nullable=False)
    short_name = db.Column(db.String(16), nullable=False)

class Departments(db.Model):
    department_id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.faculty_id'))
    full_name = db.Column(db.String(128), nullable=False)
    short_name = db.Column(db.String(16), nullable=False)
    faculty = db.relationship('Faculties', backref=db.backref('departments', lazy=True))

class Teachers(db.Model):
    teacher_id =  db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    department_id =  db.Column(db.Integer, db.ForeignKey('departments.department_id'))
    user = db.relationship('Users', backref=db.backref('teachers', uselist=False, lazy=True))
    department = db.relationship('Departments', backref=db.backref('teachers', lazy=True))

class Students_groups(db.Model):
    group_id =  db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.faculty_id'))
    name = db.Column(db.String(64), nullable=False)
    faculty = db.relationship('Faculties', backref=db.backref('students_groups', lazy=True))

class Students(db.Model):
    student_id =  db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('students_groups.group_id'))
    user = db.relationship('Users', backref=db.backref('students', uselist=False, lazy=True))
    student_group = db.relationship('Students_groups', backref=db.backref('students', lazy=True))

class Meeting(db.Model):
    meeting_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, default=datetime.now().date, nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.lesson_id'))
    theme = db.Column(db.String(128), nullable=False)
    lesson = db.relationship('Lessons', backref=db.backref('meeting', lazy=True))

class Online(db.Model):
    online_id = db.Column(db.Integer, db.ForeignKey('meeting.meeting_id'), primary_key=True)
    link_to_chat = db.Column(db.String(255))
    meeting = db.relationship('Meeting', backref=db.backref('online', uselist=False, lazy=True))

class Offline(db.Model):
    offline_id = db.Column(db.Integer, db.ForeignKey('meeting.meeting_id'), primary_key=True)
    place = db.Column(db.String(64))
    meeting = db.relationship('Meeting', backref=db.backref('offline', uselist=False, lazy=True))

class Team(db.Model):
    team_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lead_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(64), default="New team", nullable=False)
    user = db.relationship('Users', backref=db.backref('team', uselist=False, lazy=True))

class Team_members(db.Model):
    member_id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    team = db.relationship('Team', backref=db.backref('team_members', lazy=True))
    user = db.relationship('Users', backref=db.backref('team_members', lazy=True))

class Meeting_members(db.Model):
    member_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.meeting_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    meeting = db.relationship('Meeting', backref=db.backref('meeting_members', lazy=True))
    user = db.relationship('Users', backref=db.backref('meeting_members', lazy=True))

class Lessons(db.Model):
    lesson_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.String(32), nullable=False)

