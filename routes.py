from flask import Flask, redirect, render_template, request, url_for, session
from server import app
import csv, time, os.path



##classes
class Question:
    def __init__(self,text,id):
        self._text = text
        self._id = id

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self,text):
        self._text = text

    @property
    def id(self):
        return self._id


class Survey:
    def __init__(self, id, name, course, questions):
        self._id = id
        self._name = name
        self._course = course
        self._questions = questions

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,name):
        self._name = name

    @property
    def course(self):
        return self._course

    @course.setter
    def course(self,course):
        self._course = course

    @property
    def questions(self):
        return self._questions

    @questions.setter
    def questions(self,questions):
        self._questions = questions

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
        return "Not authorised! Please " + "<a href='/'>login</a>" + " first."

    questions = []

    with open('questions.csv','r') as csv_in:
      reader = csv.reader(csv_in)
      for row in reader:
          questions.append(row)

    return render_template("questions.html", questions=questions)

@app.route("/questions/add", methods=["GET", "POST"])
def addQuestion():
    if not session.get('logged_in'):
        return "Not authorised! Please " + "<a href='/'>login</a>" + " first."

    if request.method == "POST":

        question = request.form["question"]
        response1 = request.form["response1"]
        response2 = request.form["response2"]
        response3 = request.form["response3"]
        response4 = request.form["response4"]
        response5 = request.form["response5"]

        with open('questions.csv','a') as csv_out:
            writer = csv.writer(csv_out)
            writer.writerow([question, response1, response2, response3, response4, response5])

            statement = "Question has been successfully added."

        return render_template("addQuestion.html", statement = statement)


    return render_template("addQuestion.html")

@app.route("/surveys")
def surveys():
    if not session.get('logged_in'):
        return "Not authorised! Please " + "<a href='/'>login</a>" + " first."

    surveys = []

    if os.path.isfile('surveys.csv'):
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

@app.route("/survey/create", methods=["GET", "POST"])
def createSurvey():
    if not session.get('logged_in'):
        return "Not authorised! Please " + "<a href='/'>login</a>" + " first."

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
    return redirect(url_for("index"))

@app.route("/template")
def template():
    return render_template("template.html")
