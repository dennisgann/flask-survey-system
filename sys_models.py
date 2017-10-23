import csv, os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from server import db
from data_models import User, Course, Enrolment, Question, Survey, Response

class SurveySystem():

    def add_question(self, q_text, type, required, responses):
        newQ = Question(text=q_text, state=1, type=type, required=required, responses=str(responses))
        db.session.add(newQ)
        db.session.commit()
        return 1 #success

    def find_question(self, q_id):
        question = Question.query.filter_by(id=q_id).first()
        return question

    def update_question(self, q_id, q_text, state, type, required, responses):
        question = Question.query.filter_by(id=q_id).first()
        if question:
            question.text = q_text
            question.state = state
            question.type = type
            question.required = required
            question.responses = str(responses)
            db.session.commit()
            return 1
        else:
            return 0


    def create_survey(self, name, c_id, questions):
        newS = Survey(name=name, c_id=c_id, state=1, questions=str(questions))
        db.session.add(newS)
        db.session.commit()
        return 1 #success

    def update_survey(self, s_id, name, c_id, state, questions):
        survey = Survey.query.filter_by(id=s_id).first()
        if survey:
            survey.name = name
            survey.c_id = c_id
            survey.state = state
            survey.questions = str(questions)
            db.session.commit()
            return 1
        else:
            return 0

    def save_response(self, sid, responses):
        newR = Response(s_id=sid, u_id=session['user_id'], responses=str(responses))
        db.session.add(newR)
        db.session.commit()
        return 1 #success


    def create_user(self, uid, username, password, type):
        if User.query.filter_by(id=uid).first():
            return 0 #failure: user with same id already exists
        newU = User(id=uid, username=str.lower(username), password=generate_password_hash(password), type=type)
        db.session.add(newU)
        db.session.commit()
        return 1 #success

######ADDED FOR GUEST LOGIN        
    def update_user_type(self, type):
        User.type == type    
        db.session.commit() 
        
    def add_enrolment(self, uid, cid):
        newE = Enrolment(u_id=uid, c_id=cid)
        db.session.add(newE)
        db.session.commit() 
################
    def get_open_surveys(self):
        if session['user_type'] == 3:
            return Survey.query.filter_by(state = 2).all()

        else:
            enrolments = Enrolment.query.filter_by(u_id=session['user_id']).all()
            course_ids = [r[0] for r in Enrolment.query.filter_by(u_id=session['user_id']).with_entities(Enrolment.c_id).all()]
            return Survey.query.filter(Survey.c_id.in_(course_ids)).filter_by(state = 2).all()


    def get_closed_surveys(self):
        if session['user_type'] == 3:
            return Survey.query.filter_by(state = 0).all()

        else:
            enrolments = Enrolment.query.filter_by(u_id=session['user_id']).all()
            course_ids = [r[0] for r in Enrolment.query.filter_by(u_id=session['user_id']).with_entities(Enrolment.c_id).all()]
            return Survey.query.filter(Survey.c_id.in_(course_ids)).filter_by(state = 0).all()


    def get_draft_surveys(self):
        if session['user_type'] == 3:
            return Survey.query.filter_by(state = 1).all()

        else:
            enrolments = Enrolment.query.filter_by(u_id=session['user_id']).all()
            course_ids = [r[0] for r in Enrolment.query.filter_by(u_id=session['user_id']).with_entities(Enrolment.c_id).all()]
            return Survey.query.filter(Survey.c_id.in_(course_ids)).filter_by(state = 1).all()


    def csv_import(self):

        if not (os.path.isfile("data/courses.csv") and \
        os.path.isfile("data/enrolments.csv") and \
        os.path.isfile("data/passwords.csv")):
            return 0 #failure

        with open('data/courses.csv','r') as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                if not Course.query.filter_by(name=row[0], session=row[1]).first():
                    course = Course(name=row[0], session=row[1])
                    db.session.add(course)

            db.session.commit()


        with open('data/enrolments.csv','r') as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                c_id = Course.query.filter_by(name=row[1], session=row[2]).first().id
                if not c_id:
                    return 0 #failure

                if not Enrolment.query.filter_by(u_id=row[0], c_id=c_id).first():
                    enrolment = Enrolment(u_id=row[0], c_id=c_id)
                    db.session.add(enrolment)

            db.session.commit()

        with open('data/passwords.csv','r') as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                u_type = 0
                if row[2] == "student":
                    u_type = 1
                elif row[2] == "staff":
                    u_type = 2

                if not User.query.filter_by(id=row[0]).first() and u_type:
                    user = User(id=row[0], username=row[0], password=generate_password_hash(row[1]), type=u_type)
                    db.session.add(user)

            db.session.commit()

        return 1 #success


    def authenticate(self, user_name, password):
        user = User.query.filter_by(username=str.lower(user_name)).first()

        if not user:
            return False

        if check_password_hash(user.password, password):
            session['logged_in'] = True
            session['username'] = user.username
            session['user_id'] = user.id
            session['user_type'] = user.type
            return True #valid user

        return False #credentials incorrect

    def check_login(self):
        if session.get('user_type'):
                return session['user_type']
        else:
            return 0
