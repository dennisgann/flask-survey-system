##IMPORTS

from flask import Flask, redirect, render_template, request, url_for, session
from server import app
import time

from models import Question, Survey, QuestionStore, SurveyStore
from functions import check_login, check_password, check_data, get_courses


##ROUTES

#index route - login or redirect to dashboard
@app.route("/", methods=["GET", "POST"])
def index():

    if check_login():
        return render_template("dashboard.html")


    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if check_password(username, password):
            session['logged_in'] = True
            return render_template("dashboard.html")

        return render_template("login.html", error=1)

    return render_template("login.html")

#questions route - displays question pool
@app.route("/questions")
def questions():

    if not check_login(): return redirect(url_for('index'))
    check_data();

    questions = QuestionStore().active

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

    if not check_login(): return redirect(url_for('index'))
    check_data();

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

    if not check_login(): return redirect(url_for('index'))

    if request.method == "POST":

        qID =  str(int(time.time()))
        qText = request.form["question"]
        responses = list(filter(None, request.form.getlist("responses")))

        if qText.isspace() or qText == "" or len(responses) < 2 or all(responses[i].isspace() for i in range(0, len(responses)-1)):
            return render_template("addQuestion.html", error=1)

        question = Question(qID,1,qText,responses)

        if QuestionStore().add(question):
            return render_template("addQuestion.html", success=1)
        else:
            return render_template("addQuestion.html", error=2)

    return render_template("addQuestion.html")

#displays surveys - both active and inactive
@app.route("/surveys")
def surveys():

    if not check_login(): return redirect(url_for('index'))
    check_data();

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

    if not check_login(): return redirect(url_for('index'))
    check_data();

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

    if not check_login(): return redirect(url_for('index'))
    check_data();

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
            return render_template("createSurvey.html", questions=questions, courses=courses, success=1)
        else:
            return render_template("createSurvey.html", questions=questions, courses=courses, error=2)

    else:
        return render_template("createSurvey.html", questions=questions, courses=courses)


#survey page (public) - allows reponses to be collected
@app.route("/survey/<sid>")
def survey(sid):
    check_data();

    survey = SurveyStore().find(sid)

    questions = []

    for questionID in survey.questions:
        questions.append(QuestionStore().find(questionID))

    survey.questions = questions

    return render_template("survey.html", survey=survey)


#logout - destroys session and redirects to index/login
@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.clear()
    return redirect(url_for("index"))
