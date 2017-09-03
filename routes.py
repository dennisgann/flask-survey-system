##Code by Dennis Gann

from flask import Flask, redirect, render_template, request, url_for, session
from server import app
import csv, time, os.path

##login
users = {"admin": "password"}

class Question:
    def __init__(self,text):
        self._text = text
        self._id = id

    def _get_question(self):
        return _text

    def _set_question(text, id):
        self._text = text
        self._id = id

    question = property(_get_question,_set_question)

OR

class Question:
    def __init__(self,text):
        self._text = text
        self._id = id

    @property
    def question(self):
        return self._text

    @property.setter
    def question(text, id):
        self._text = text
        self._id = id

#Not sure how to implement a list into a class - sorry
class Survey:
    def __init__(self, id, name, course, questions):
        self._id = id
        self._name = name
        self._course = course 
        self._questions = questions

    def _get_survey(self):
        return self._id + ' ' + self.name + ' ' + self.course + ' ' + self.questions
    
    def _set_survey(self, id, name, course, questions):
        self._id = id
        self._name = name
        self._course = course
        self._questions = questions
    
    survey = property(_get_survey,_set_survey)

def check_password(user_name, password):
    if password == users[user_name]:
        return True
    return False

@app.route("/", methods=["GET", "POST"])
def index():

    if session['logged_in']:
        return render_template("dashboard.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if check_password(username, password):
            session['logged_in'] = True
            return render_template("dashboard.html")

        return "Your username/password combination was incorrect."

    return render_template("login.html")

@app.route("/questions")
def questions():
    if not session['logged_in']:
        return "Not authorised! Please " + "<a href='/'>login</a>" + " first."

    questions = []

    with open('questions.csv','r') as csv_in:
      reader = csv.reader(csv_in)
      for row in reader:
          questions.append(row)

    return render_template("questions.html", questions=questions)

@app.route("/questions/add", methods=["GET", "POST"])
def addQuestion():
    if not session['logged_in']:
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
    if not session['logged_in']:
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
    if not session['logged_in']:
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
