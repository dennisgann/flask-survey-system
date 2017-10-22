import ast
from datetime import datetime
from server import db

class User(db.Model):

    __tablename__ = 'USERS'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Integer, nullable=False)

class Course(db.Model):

    __tablename__ = 'COURSES'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(10), nullable=False)
    session = db.Column(db.String(5), nullable=False)

class Enrolment(db.Model):

    __tablename__ = 'ENROLMENTS'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    u_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    c_id = db.Column(db.Integer, db.ForeignKey(Course.id), nullable=False)
    user = db.relationship(User)
    course = db.relationship(Course)

class Question(db.Model):

    __tablename__ = 'QUESTIONS'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    state = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    required = db.Column(db.Integer, nullable=False)
    responses = db.Column(db.Text, nullable=False)

    def responsesList(self):
         return ast.literal_eval(self.responses)

class Survey(db.Model):

    __tablename__ = 'SURVEYS'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    c_id = db.Column(db.Integer, db.ForeignKey(Course.id), nullable=False)
    state = db.Column(db.Integer, nullable=False)
    questions = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now())
    course = db.relationship(Course)

    def questionsList(self):
         return ast.literal_eval(self.questions)

class Response(db.Model):

    __tablename__ = 'RESPONSES'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    u_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    s_id = db.Column(db.Integer, db.ForeignKey(Survey.id), nullable=False)
    responses = db.Column(db.Text, nullable=False)
    user = db.relationship(User)
    survey = db.relationship(Survey)

    def responsesList(self):
         return ast.literal_eval(self.responses)
