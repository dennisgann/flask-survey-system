##pyChart - UNSW COMP1531 17s2 Group Project
##Created by Frank Foo, Dennis Gann and Charmaine Leung

##IMPORTS
from flask import Flask, redirect, render_template, request, url_for, session
from server import app, db

from data_models import User, Course, Enrolment, Question, Survey, Response
from sys_models import SurveySystem

system = SurveySystem()

##ROUTES

#index route - login or redirect to dashboard
@app.route("/", methods=["GET", "POST"])
def index():

    if system.check_login() == 1:
        enrolments = Enrolment.query.filter_by(u_id=session['user_id']).all()
        open_surveys = system.get_open_surveys()
        closed_surveys = system.get_closed_surveys()
        return render_template("studentDashboard.html", enrolments=enrolments, active_surveys=open_surveys, inactive_surveys=closed_surveys)

    elif system.check_login() == 2:
        enrolments = Enrolment.query.filter_by(u_id=session['user_id']).all()
        draft_surveys = system.get_draft_surveys()
        closed_surveys = system.get_closed_surveys()
        return render_template("staffDashboard.html", enrolments=enrolments, draft_surveys=draft_surveys, inactive_surveys=closed_surveys)

    elif system.check_login() == 3:
        return render_template("adminDashboard.html")


    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if system.authenticate(username, password):
            return redirect(url_for("index"))

        return render_template("login.html", error=1)

    return render_template("login.html") 
    
#guest register route - displays guest registration
@app.route("/register", methods=["GET", "POST"])
def register():

    courses = Course.query.all()
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        course = request.form["course"]
        
        gid = User.query.order_by(User.id.desc()).first().id
        
        system.create_user(gid+1,username, password, 5)
        system.add_enrolment(gid+1, course)
            
        return render_template("registerGuest.html", success=1, courses=courses)
    
    return render_template("registerGuest.html", courses=courses)
            
#approval route - displays guests awaiting approval
@app.route("/approve", methods=["GET", "POST"])
def approve():
    if not system.check_login() == 3: return redirect(url_for('index'))
    
    guest_requests = User.query.filter_by(type=5).all()
    
    if request.method == "POST":
        approved_user = request.form['guest']
        approved_user.system.update_user_type(4)
    
    return render_template("approveGuest.html", guest_requests = guest_requests, Enrolment=Enrolment)
    
    

#questions route - displays question pool
@app.route("/questions")
def questions():

    if not system.check_login() == 3: return redirect(url_for('index'))

    mandatory_questions = Question.query.filter_by(state = 1, required = 1).all()
    optional_questions = Question.query.filter_by(state = 1, required = 0).all()

    if request.args.get('delete'):
        if request.args.get('delete') == '1':
            return render_template("questions.html", mandatory_questions=mandatory_questions, optional_questions=optional_questions, success=1)
        else:
            return render_template("questions.html", mandatory_questions=mandatory_questions, optional_questions=optional_questions, error=1)
    else:
        return render_template("questions.html", mandatory_questions=mandatory_questions, optional_questions=optional_questions)


#delete question - deletest question from pool and redirects back to questions
@app.route("/questions/delete/<qid>")
def delQuestion(qid):

    if not system.check_login() == 3: return redirect(url_for('index'))

    delete = 0
    delQuestion = Question.query.filter_by(id=qid).first()

    if delQuestion:
        if system.update_question(qid, delQuestion.text, 0, delQuestion.type, \
        delQuestion.required, delQuestion.responses):
            delete = 1

    return redirect(url_for("questions", delete=delete))


#add question - adds question to pool
@app.route("/questions/add", methods=["GET", "POST"])
def addQuestion():

    if not system.check_login() == 3: return redirect(url_for('index'))

    if request.method == "POST":

        qText = request.form["question"]
        responses = list(filter(None, request.form.getlist("responses")))
        qType = 1
        if request.form["type"] == 'Text':
            qType = 2
            responses = []
        required = 1
        if request.form['optional'] == '1':
            required = 0

        if qText.isspace() or qText == "" or qType == 1 and (len(responses) < 2 or all(responses[i].isspace() for i in range(0, len(responses)-1))):
            return render_template("addQuestion.html", error=1)


        if system.add_question(qText, qType, required, responses):
            return render_template("addQuestion.html", success=1)
        else:
            return render_template("addQuestion.html", error=2)

    return render_template("addQuestion.html")


#displays surveys - both active and inactive
@app.route("/surveys")
def surveys():

    if not system.check_login() == 3: return redirect(url_for('index'))

    draft_surveys = system.get_draft_surveys()
    active_surveys = system.get_open_surveys()
    inactive_surveys = system.get_closed_surveys()

    if request.args.get('close'):
        if request.args.get('close') == '1':
            return render_template("surveys.html", draft_surveys=draft_surveys, active_surveys=active_surveys, inactive_surveys=inactive_surveys, success=1)
        else:
            return render_template("surveys.html", draft_surveys=draft_surveys, active_surveys=active_surveys, inactive_surveys=inactive_surveys, error=1)
    else:
        return render_template("surveys.html", draft_surveys=draft_surveys, active_surveys=active_surveys, inactive_surveys=inactive_surveys)


#close survey - makes survey inactive and redirects to surveys page
@app.route("/surveys/close/<sid>")
def closeSurvey(sid):

    if not system.check_login() == 3: return redirect(url_for('index'))

    close = 0

    closeSurvey = Survey.query.filter_by(id=sid).first()

    if closeSurvey:
        if system.update_survey(sid, closeSurvey.name, closeSurvey.c_id, 0, closeSurvey.questions):
            close = 1

    return redirect(url_for("surveys", close=close))


#review survey
@app.route("/surveys/review/<sid>", methods=["GET", "POST"])
def reviewSurvey(sid):

    if not system.check_login() == 2: return redirect(url_for('index'))

    course_ids = [r[0] for r in Enrolment.query.filter_by(u_id=session['user_id']).with_entities(Enrolment.c_id).all()]

    survey = Survey.query.filter_by(id=sid).first()

    if not survey: return render_template("review.html", error=3)

    if survey.c_id not in course_ids:
        return redirect(url_for('index'))

    questions = []
    for questionID in survey.questionsList():
        questions.append(system.find_question(questionID))

    optional_questions = Question.query.filter(Question.id.notin_(survey.questionsList())).filter_by(state = 1, required = 0).all()

    if request.method == "POST":

        s_questions = survey.questionsList()
        for question in optional_questions:
            response = request.form.get(str(question.id))
            if response:
                s_questions.append(response)


        if system.update_survey(sid, survey.name, survey.c_id, 2, s_questions):
            return render_template("review.html", survey=survey, questions=questions, optional_questions=optional_questions, success=1)
        else:
            return render_template("review.html", survey=survey, questions=questions, optional_questions=optional_questions, error=0)

    else:
        return render_template("review.html", survey=survey, questions=questions, optional_questions=optional_questions)


#create survey - captures input a creats a new survey object in SurveyStore
@app.route("/surveys/create", methods=["GET", "POST"])
def createSurvey():

    if not system.check_login() == 3: return redirect(url_for('index'))

    questions = Question.query.filter_by(state = 1).all()
    courses = Course.query.all()

    if request.method == "POST":

        surveyName = request.form["name"]
        surveyCourse = request.form["course"]
        surveyQs = request.form.getlist("questions")

        if surveyName.isspace() or surveyName == "" or not surveyQs or not surveyCourse:
            return render_template("createSurvey.html", questions=questions, courses=courses, error=1)


        if system.create_survey(surveyName, surveyCourse, surveyQs):
            return render_template("createSurvey.html", questions=questions, courses=courses, success=1)
        else:
            return render_template("createSurvey.html", questions=questions, courses=courses, error=2)

    else:
        return render_template("createSurvey.html", questions=questions, courses=courses)


#survey page - allows responses to be collected
@app.route("/survey/<sid>", methods=["GET", "POST"])
def survey(sid):

    if not system.check_login() == 1: return redirect(url_for('index'))
    #check whether student is enrolled in course and hasn't already taken survey
    course_ids = [r[0] for r in Enrolment.query.filter_by(u_id=session['user_id']).with_entities(Enrolment.c_id).all()]

    survey = Survey.query.filter_by(id=sid).first()

    if survey.c_id not in course_ids:
        return redirect(url_for('index'))

    if not survey: return render_template("survey.html", error=3)

    if Response.query.filter_by(s_id=sid, u_id=session['user_id']).first():
        return render_template("survey.html", survey=survey, success=1)


    questions = []
    for questionID in survey.questionsList():
        questions.append(system.find_question(questionID))

    if request.method == "POST":

        responses = []
        for question in questions:
            response = request.form.get(str(question.id))
            if question.required and (response == None or response.isspace() or response == ""):
                return render_template("survey.html", survey=survey, questions=questions, error=1)

            if question.type == 1 and response == None:
                response = '0'

            #need to add checking of returned value for MCQ (type == 1) ie. 1 <= val <= noResponses

            responses.append(response)


        if system.save_response(sid, responses):
            return render_template("survey.html", survey=survey, questions=questions, success=1)
        else:
            return render_template("survey.html", survey=survey, questions=questions, error=2)

    else:
        return render_template("survey.html", survey=survey, questions=questions)


#results page - show survey results
@app.route("/results/<sid>")
def results(sid):

    return 


#logout - destroys session and redirects to index/login
@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['username'] = ""
    session['user_id'] = ""
    session['user_type'] = 0
    session.clear()
    return redirect(url_for("index"))

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("index"))
