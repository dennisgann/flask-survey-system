##Code by Dennis Gann

from flask import Flask, redirect, render_template, request, url_for, session
from server import app
import csv, time

##login
users = {"admin": "password"}

def check_password(user_name, password):
    if password == users[user_name]:
        return True
    return False

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if check_password(username, password):
            session['logged_in'] = True
            return "You are now authenticated."

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

        return "Question has been successfully added."


    return render_template("addQuestion.html")


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
            writer.writerow([survey_name, course, questions])

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
