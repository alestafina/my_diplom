from Meeting import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
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
    teacher_id =  db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    department_id =  db.Column(db.Integer, db.ForeignKey('departments.department_id'))
    user = db.relationship('User', backref=db.backref('teachers', uselist=False, lazy=True))
    department = db.relationship('Departments', backref=db.backref('teachers', lazy=True))

class Students_groups(db.Model):
    group_id =  db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.faculty_id'))
    name = db.Column(db.String(64), nullable=False)
    faculty = db.relationship('Faculties', backref=db.backref('students_groups', lazy=True))

class Students(db.Model):
    student_id =  db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('students_groups.group_id'))
    user = db.relationship('User', backref=db.backref('students', uselist=False, lazy=True))
    student_group = db.relationship('Students_groups', backref=db.backref('students', lazy=True))

class Meeting(db.Model):
    meeting_id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    theme = db.Column(db.String(128), nullable=False)

class Online(db.Model):
    online_id = db.Column(db.Integer, db.ForeignKey('meeting.meeting_id'), primary_key=True)
    link_to_chat = db.Column(db.String(255))
    meeting = db.relationship('Meeting', backref=db.backref('online', uselist=False, lazy=True))

class Offline(db.Model):
    offline_id = db.Column(db.Integer, db.ForeignKey('meeting.meeting_id'), primary_key=True)
    place = db.Column(db.String(64))
    meeting = db.relationship('Meeting', backref=db.backref('offline', uselist=False, lazy=True))

class Comand(db.Model):
    comand_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), default="New comand", nullable=False)

class Comand_members(db.Model):
    member_id = db.Column(db.Integer, primary_key=True) 
    command_id = db.Column(db.Integer, db.ForeignKey('comand.comand_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    command = db.relationship('Comand', backref=db.backref('comand_members', lazy=True))
    user = db.relationship('User', backref=db.backref('comand_members', lazy=True))

class Meeting_members(db.Model):
    member_id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.meeting_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    meeting = db.relationship('Meeting', backref=db.backref('meeting_members', lazy=True))
    user = db.relationship('User', backref=db.backref('meeting_members', lazy=True))

