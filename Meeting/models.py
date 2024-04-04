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
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'))
    full_name = db.Column(db.String(128), nullable=False)
    short_name = db.Column(db.String(16), nullable=False)

class Teachers(db.Model):
    teacher_id =  db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    department_id =  db.Column(db.Integer, db.ForeignKey('departments.department_id'))

class Students_groups(db.Model):
    group_id =  db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.faculty_id'))
    name = db.Column(db.String(64), nullable=False)

class Students(db.Model):
    student_id =  db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('students_groups.group_id'))

class Meeting(db.Model):
    meeting_id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    theme = db.Column(db.String(128), nullable=False)

class Online(db.Model):
    online_id = db.Column(db.Integer, db.ForeignKey('meeting.meeting_id'), primary_key=True)
    link_to_chat = db.Column(db.String(255))

class Offline(db.Model):
    offline_id = db.Column(db.Integer, db.ForeignKey('meeting.meeting_id'), primary_key=True)
    place = db.Column(db.String(64))

class Comand(db.Model):
    comand_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), default="New comand", nullable=False)

class Comand_members(db.Model):
    command_id = db.Column(db.Integer, db.ForeignKey('comand.comand_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Meeting_members(db.Model):
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.meeting_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))

