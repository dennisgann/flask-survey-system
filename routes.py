##pyChart - UNSW COMP1531 17s2 Group Project
##Created by Frank Foo, Dennis Gann and Charmaine Leung

##IMPORTS

from flask import Flask, redirect, render_template, request, url_for, session
from server import app, db
import time

from models import User, Course, Enrolment, Question, Survey, Response, SurveySystem

system = SurveySystem()

##ROUTES

#index route - login or redirect to dashboard
@app.route("/", methods=["GET", "POST"])
def index():

    if system.check_login():
        return render_template("dashboard.html")


    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]


        if system.authenticate(username, password):
            return render_template("dashboard.html")

        return render_template("login.html", error=1)

    return render_template("login.html")


#questions route - displays question pool
@app.route("/questions")
def questions():

    if not system.check_login(): return redirect(url_for('index'))

    questions = Question.query.filter_by(state = 1).all()

    if request.args.get('delete'):
        if request.args.get('delete') == '1':
            return render_template("questions.html", questions=questions, success=1)
        else:
            return render_template("questions.html", questions=questions, error=1)
    else:
        return render_template("questions.html", questions=questions)


#delete question - deletest question from pool and redirects back to questions
@app.route("/questions/delete/<qid>")
def delQuestion(qid):

    if not system.check_login(): return redirect(url_for('index'))

    delete = 0

    delQuestion = QuestionStore().find(qid)

    if delQuestion:
        delQuestion.state = '0'
        delete = 1
        QuestionStore().update(delQuestion)

    return redirect(url_for("questions", delete=delete))


#add question - adds question to pool
@app.route("/questions/add", methods=["GET", "POST"])
def addQuestion():

    if not system.check_login(): return redirect(url_for('index'))

    if request.method == "POST":

        qText = request.form["question"]
        qType = 1
        required = 1
        responses = list(filter(None, request.form.getlist("responses")))

        if qText.isspace() or qText == "" or len(responses) < 2 or all(responses[i].isspace() for i in range(0, len(responses)-1)):
            return render_template("addQuestion.html", error=1)


        if system.add_question(qText, qType, required, responses):
            return render_template("addQuestion.html", success=1)
        else:
            return render_template("addQuestion.html", error=2)

    return render_template("addQuestion.html")


#displays surveys - both active and inactive
@app.route("/surveys")
def surveys():

    if not system.check_login(): return redirect(url_for('index'))

    active_surveys = SurveyStore().active
    inactive_surveys = SurveyStore().inactive

    if request.args.get('close'):
        if request.args.get('close') == '1':
            return render_template("surveys.html", active_surveys=active_surveys, inactive_surveys=inactive_surveys, success=1)
        else:
            return render_template("surveys.html", active_surveys=active_surveys, inactive_surveys=inactive_surveys, error=1)
    else:
        return render_template("surveys.html", active_surveys=active_surveys, inactive_surveys=inactive_surveys)


#close survey - makes survey inactive and redirects to surveys page
@app.route("/surveys/close/<sid>")
def closeSurvey(sid):

    if not system.check_login(): return redirect(url_for('index'))

    close = 0

    closeSurvey = SurveyStore().find(sid)

    if closeSurvey:
        closeSurvey.state = '0'
        close = 1
        SurveyStore().update(closeSurvey)

    return redirect(url_for("surveys", close=close))


#create survey - captures input a creats a new survey object in SurveyStore
@app.route("/surveys/create", methods=["GET", "POST"])
def createSurvey():

    if not system.check_login(): return redirect(url_for('index'))

    questions = QuestionStore().active
    courses = get_courses()

    if request.method == "POST":

        surveyName = request.form["name"]
        surveyCourse = request.form["course"]
        surveyQs = request.form.getlist("questions")
        surveyID =  str(int(time.time()))

        if surveyName.isspace() or surveyName == "" or not surveyQs:
            return render_template("createSurvey.html", questions=questions, courses=courses, error=1)

        survey = Survey(surveyID, 1, surveyName, surveyCourse, surveyQs)

        if SurveyStore().add(survey):
            return render_template("createSurvey.html", questions=questions, courses=courses, success=1, survey=survey)
        else:
            return render_template("createSurvey.html", questions=questions, courses=courses, error=2)

    else:
        return render_template("createSurvey.html", questions=questions, courses=courses)


#survey page (public) - allows reponses to be collected
@app.route("/survey/<sid>", methods=["GET", "POST"])
def survey(sid):

    survey = SurveyStore().find(sid)

    if not survey: return render_template("survey.html", survey=survey, error=3)

    questions = []

    for questionID in survey.questions:
        questions.append(QuestionStore().find(questionID))

    survey.questions = questions

    if request.method == "POST":

        responses = list(request.form.values())[:-1]

        if len(responses) != len(survey.questions):
            return render_template("survey.html", survey=survey, error=1)

        if write_response(sid, responses):
            return render_template("survey.html", survey=survey, success=1)
        else:
            return render_template("survey.html", survey=survey, error=2)

    else:
        return render_template("survey.html", survey=survey)


#logout - destroys session and redirects to index/login
@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['username'] = ""
    session['user_id'] = ""
    session['user_type'] = 0
    session.clear()
    return redirect(url_for("index"))
