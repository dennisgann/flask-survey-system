from flask import Flask, redirect, render_template, request, url_for, session
import csv, time
from server import app
from Question import Question

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

    surveys = []

    with open('surveys.csv','r') as csv_in:
      reader = csv.reader(csv_in)
      for row in reader:
          surveys.append(row)

    return render_template("surveys.html", surveys=surveys)

@app.route("/survey/<id>")
def survey(id):

    survey = []

    with open('surveys/' + id + '.csv','r') as csv_in:
      reader = csv.reader(csv_in)
      for row in reader:
          survey.append(row)


    return render_template("survey.html", survey=survey)

@app.route("/surveys/create", methods=["GET", "POST"])
def createSurvey():
    if not session.get('logged_in'):
        return redirect(url_for("index"))

    if request.method == "POST":

        survey_name = request.form["name"]
        course = request.form["course"]
        questions = request.form.getlist("questions")

        surveyID =  str(int(time.time()))
        with open('surveys/' +  surveyID + '.csv','w') as csv_out:
            writer = csv.writer(csv_out)
            writer.writerow([survey_name, course])
            writer.writerow(questions)

        with open('surveys.csv','a') as csv_out:
            writer = csv.writer(csv_out)
            writer.writerow([surveyID, survey_name, course, 1])

        return "Successfully created survey with ID: " + surveyID

    questions = []

    with open('questions.csv','r') as csv_in:
      reader = csv.reader(csv_in)
      for row in reader:
          questions.append(row)

    courses = []

    with open('courses.csv','r') as csv_in:
        reader = csv.reader(csv_in)
        next(reader)
        for row in reader:
            if row:
                courses.append(row)

    return render_template("createSurvey.html", questions=questions, courses=courses)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    session.clear()
    return redirect(url_for("index"))
