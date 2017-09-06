import os.path, csv
from flask import session

##FUNCTIONS


##login functions
users = {"admin": "password"}

def check_password(user_name, password):
    if users.get(user_name) == password:
        return True
    return False

def check_login():
    if session.get('logged_in'):
            return True
    else:
        return False


##csv file check function
def check_data():
    if not os.path.isfile("data/questions.csv"):
        with open("data/questions.csv", "w") as q_csv:
            pass
    if not os.path.isfile("data/surveys.csv"):
        with open("data/surveys.csv", "w") as s_csv:
            pass
    if not os.path.isfile("data/courses.csv"):
        with open("data/courses.csv", "w") as c_csv:
            pass


##get courses from csv
def get_courses():
    courses = []
    with open('data/courses.csv','r') as csv_in:
        reader = csv.reader(csv_in)
        for row in reader:
            if row:
                courses.append(row)
    return courses


##write survey responses
def write_response(sid, response):
    with open('data/' + sid + '.csv','a') as csv_out:
        writer = csv.writer(csv_out)
        writer.writerow(response)
        return 1 #success

    return 0 #failure
