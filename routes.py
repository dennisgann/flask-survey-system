from flask import Flask, redirect, render_template, request, url_for, session
import csv, time
from server import app
from Question import Question
from Survey import Survey

##login
users = {"admin": "password"}

def check_password(user_name, password):
    if users.get(user_name) == password:
        return True
    return False


##routes
@app.route("/", methods=["GET", "POST"])
def index():

    if session.get('logged_in'):
        return render_template("dashboard.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if check_password(username, password):
            session['logged_in'] = True
            return render_template("dashboard.html")

        return render_template("login.html", error=1)

    return render_template("login.html")

@app.route("/questions")
def questions():
    if not session.get('logged_in'):
        return redirect(url_for("index"))

    questions = []

    with open('questions.csv','r') as csv_in:
      reader = csv.reader(csv_in)
      for row in reader:
          if row[1] == '1':
              question = Question(row[0], row[1], row[2], row[3:])
              questions.append(question)

    if request.args.get('delete'):
        if request.args.get('delete') == '1':
            return render_template("questions.html", questions=questions, success=1)
        else:
            return render_template("questions.html", questions=questions, error=1)
    else:
        return render_template("questions.html", questions=questions)

@app.route("/questions/delete/<qid>")
def delQuestion(qid):
    if not session.get('logged_in'):
        return redirect(url_for("index"))

    questions = []
    delete = 0

    with open('questions.csv','r') as csv_in:
      reader = csv.reader(csv_in)
      for row in reader:
          if row[0] == qid and row[1] == '1':
              question = Question(row[0], 0, row[2], row[3:])
              questions.append(question)
              delete = 1
          else:
              question = Question(row[0], row[1], row[2], row[3:])
              questions.append(question)


    with open('questions.csv', "w") as csv_out:
        csv_out.truncate()

    for question in questions:
        question.write()

    return redirect(url_for("questions", delete=delete))

@app.route("/questions/add", methods=["GET", "POST"])
def addQuestion():
    if not session.get('logged_in'):
        return redirect(url_for("index"))

    if request.method == "POST":

        qID =  str(int(time.time()))
        qText = request.form["question"]
        responses = list(filter(None, request.form.getlist("responses")))

        if qText.isspace() or qText == "" or len(responses) < 2 or all(responses[i].isspace() for i in range(0, len(responses)-1)):
            return render_template("addQuestion.html", error=1)

        question = Question(qID,1,qText,responses)

        if question.write():
            return render_template("addQuestion.html", success=1)
        else:
            return render_template("addQuestion.html", error=2)


    return render_template("addQuestion.html")

@app.route("/surveys")
def surveys():
    if not session.get('logged_in'):
        return redirect(url_for("index"))

    active_surveys = []
    inactive_surveys = []

    with open('surveys.csv','r') as csv_in:
      reader = csv.reader(csv_in)
      for row in reader:
              survey = Survey(row[0], row[1], row[2], row[3], [])
              if survey.state == '1':
                  active_surveys.append(survey)
              else:
                  inactive_surveys.append(survey)

    if request.args.get('close'):
        if request.args.get('close') == '1':
            return render_template("surveys.html", active_surveys=active_surveys, inactive_surveys=inactive_surveys, success=1)
        else:
            return render_template("surveys.html", active_surveys=active_surveys, inactive_surveys=inactive_surveys, error=1)
    else:
        return render_template("surveys.html", active_surveys=active_surveys, inactive_surveys=inactive_surveys)


@app.route("/surveys/close/<sid>")
def closeSurvey(sid):
    if not session.get('logged_in'):
        return redirect(url_for("index"))

    surveys = []
    close = 0

    with open('surveys.csv','r') as csv_in:
      reader = csv.reader(csv_in)
      for row in reader:
          if row[0] == sid and row[1] == '1':
              survey = Survey(row[0], 0, row[2], row[3], [])
              surveys.append(survey)
              close = 1
          else:
              survey = Survey(row[0], row[1], row[2], row[3], [])
              surveys.append(survey)


    with open('surveys.csv', "w") as csv_out:
        csv_out.truncate()

    for survey in surveys:
        survey.write()

    return redirect(url_for("surveys", close=close))



@app.route("/surveys/create", methods=["GET", "POST"])
def createSurvey():
    if not session.get('logged_in'):
        return redirect(url_for("index"))

    questions = []

    with open('questions.csv','r') as csv_in:
      reader = csv.reader(csv_in)
      for row in reader:
          if row[1] == '1':
              question = Question(row[0], row[1], row[2], row[3:])
              questions.append(question)

    courses = []

    with open('courses.csv','r') as csv_in:
        reader = csv.reader(csv_in)
        next(reader)
        for row in reader:
            if row:
                courses.append(row)


    if request.method == "POST":

        surveyName = request.form["name"]
        surveyCourse = request.form["course"]
        surveyQs = request.form.getlist("questions")
        surveyID =  str(int(time.time()))
        survey = Survey(surveyID, 1, surveyName, surveyCourse, surveyQs)

        if surveyName.isspace() or surveyName == "" or not surveyQs:
            return render_template("createSurvey.html", questions=questions, courses=courses, error=1)

        if survey.write():
            return render_template("createSurvey.html", questions=questions, courses=courses, success=1)
        else:
            return render_template("createSurvey.html", questions=questions, courses=courses, error=2)


    return render_template("createSurvey.html", questions=questions, courses=courses)


@app.route("/survey/<sid>")
def survey(sid):

    with open('surveys/' + sid + '.csv','r') as csv_in:
      reader = csv.reader(csv_in)
      row1 = next(reader)
      row2 = next(reader)
      questions = []
      with open('questions.csv','r') as csv_in:
        reader = csv.reader(csv_in)
        for row in reader:
            if row[0] in row2:
                question = Question(row[0], row[1], row[2], row[3:])
                questions.append(question)

      survey = Survey(sid,'1',row1[1],row1[2],questions)

      return render_template("survey.html", survey=survey)




@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.clear()
    return redirect(url_for("index"))
