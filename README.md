# pyChart Survey System
Frank Foo, Dennis Gann, Charmaine Leung

COMP1531 17s2 Group Project
Tutorial H13A

# Section 1: Dependencies
External Python libraries:
- Flask 0.12.2 (http://flask.pocoo.org)
- Flask SQLAlchemy 2.3.1 (http://flask-sqlalchemy.pocoo.org/2.3/)
CSS and JS:
- Pure.css 1.0.0 (https://purecss.io)
- Google Charts (https://developers.google.com/chart/)


# Section 2: Setup instructions
1. Unzip archive into new empty directory
2. Ensure data/ directory contains the following CSV files: courses.csv, enrolments.csv & passwords.csv (update if necessary)
3. Setup a python3 virtual environment ($ virtualenv --python=/usr/local/bin/python3 env)
4. Activate virtual environment ($ source env/bin/activate)
5. PIP install flask & flask-sqlalchemy ($ pip install flask) ($ pip install flask-sqlalchemy)
6. Run application ($ python run.py)
    --> application will start on localhost:1234 or whichever port is set in the run.py file
    --> N.B. the run.py script will import changes from CSV files, this can take some time, especially when running for the first time. Please be patient.

- URL of home page: http://127.0.0.1:1234 or http://localhost:1234


# Section 3: Tests
- contained in tests/


# Suggested Login credentials:

The following credentials will allow you to play around with various user roles.
Start by creating a survey for COMP1000 17s2, since they all have this course in common.

- ROLE: USERNAME / PASSWORD
- Admin: admin / password
- Staff: 80 / staff880
- Student: 100 / student228
