import unittest
from server import db
from sys_models import *
from data_models import *


#=========================================
#Test cases for core User stories:
#(1) Create Mandatory/Optional Questions
#(2) Create a survey
#(3) Enrol a user
#(4) Create user (ie. guest or csv import)
#(5) Authenticate user
#=========================================


#(1) Testing adding questions to the generic pool
class TestAddQuestion(unittest.TestCase):

    def setUp(self):
        db.create_all()
        self.system = SurveySystem()
        self.system.csv_import()

    def test_add_question_invalid_text(self):
        """
        Add question without Q text
        post: There will be no changes in the database
        """
        print("Add question without Q text")
        q_text = ""
        q_type = 1
        q_required = 1
        q_responses =  ["Yes", "No"]

        prev_noQuestions = len(Question.query.all())
        self.assertEqual(self.system.add_question(q_text, q_type, q_required, q_responses), 0)
        curr_noQuestions = len(Question.query.all())
        self.assertEqual(prev_noQuestions, curr_noQuestions)

    def test_add_question_invalid_responses(self):
        """
        Add MCQ question without responses
        post: There will be no changes in the database
        """
        print("Add MCQ question without responses")
        q_text = "Test 9999"
        q_type = 1
        q_required = 1
        q_responses =  []

        prev_noQuestions = len(Question.query.all())
        self.assertEqual(self.system.add_question(q_text, q_type, q_required, q_responses), 0)
        curr_noQuestions = len(Question.query.all())
        self.assertEqual(prev_noQuestions, curr_noQuestions)

    def test_add_question_invalid_type(self):
        """
        Add question with invalid type
        post: There will be no changes in the database
        """
        print("Add question with invalid type")
        q_text = "Test 9999"
        q_type = 5
        q_required = 0
        q_responses =  ["Yes", "No"]

        prev_noQuestions = len(Question.query.all())
        self.assertEqual(self.system.add_question(q_text, q_type, q_required, q_responses), 0)
        curr_noQuestions = len(Question.query.all())
        self.assertEqual(prev_noQuestions, curr_noQuestions)

    def test_add_optional_valid(self):
        """
        Add optional question
        post: There will be changes in the database
        """
        print("Add optional question")
        q_text = "Test 9999"
        q_type = 1
        q_required = 0
        q_responses =  ["Yes", "No"]

        prev_noQuestions = len(Question.query.all())
        self.assertEqual(self.system.add_question(q_text, q_type, q_required, q_responses), 1)
        curr_noQuestions = len(Question.query.all())
        self.assertEqual(prev_noQuestions + 1, curr_noQuestions)

    def test_add_mandatory_valid(self):
        """
        Add Mandatory question
        post: There will be changes in the database
        """
        print("Add Mandatory question")
        q_text = "Test 9999"
        q_type = 2
        q_required = 1
        q_responses =  []

        prev_noQuestions = len(Question.query.all())
        self.assertEqual(self.system.add_question(q_text, q_type, q_required, q_responses), 1)
        curr_noQuestions = len(Question.query.all())
        self.assertEqual(prev_noQuestions + 1, curr_noQuestions)


#(2) Test cases for survey creation
class TestCreateSurvey(unittest.TestCase):

    def setUp(self):
        db.create_all()
        self.system = SurveySystem()
        self.system.csv_import()

    def test_create_invalid_name(self):
        """
        Create survey with invalid name
        pre: valid course id
        post: There will be no changes in the database
        """
        print("Create survey with invalid name")
        s_name = ""
        c_id = 1
        questions = [1, 2]

        prev_noSurveys = len(Survey.query.all())
        self.assertEqual(self.system.create_survey(s_name, c_id, questions), 0)
        curr_noSurveys = len(Survey.query.all())
        self.assertEqual(prev_noSurveys, curr_noSurveys)

    def test_create_invalid_courseId(self):
        """
        Create survey with invalid course id
        post: There will be no changes in the database
        """
        print("Create survey with invalid course id")
        s_name = "Test 9999"
        c_id = 1000
        questions = [1, 2]

        prev_noSurveys = len(Survey.query.all())
        self.assertEqual(self.system.create_survey(s_name, c_id, questions), 0)
        curr_noSurveys = len(Survey.query.all())
        self.assertEqual(prev_noSurveys, curr_noSurveys)

    def test_create_invalid_questions(self):
        """
        Create survey with invalid questions
        pre: valid course id
        post: There will be no changes in the database
        """
        print("Create survey with invalid questions")
        s_name = ""
        c_id = 1
        questions = []

        prev_noSurveys = len(Survey.query.all())
        self.assertEqual(self.system.create_survey(s_name, c_id, questions), 0)
        curr_noSurveys = len(Survey.query.all())
        self.assertEqual(prev_noSurveys, curr_noSurveys)

    def test_create_valid_survey(self):
        """
        Create valid survey
        pre: valid course id
        post: There will be changes in the database
        """
        print("Create valid survey")
        s_name = "Test 9999"
        c_id = 1
        questions = [1, 2]

        prev_noSurveys = len(Survey.query.all())
        self.assertEqual(self.system.create_survey(s_name, c_id, questions), 1)
        curr_noSurveys = len(Survey.query.all())
        self.assertEqual(prev_noSurveys + 1, curr_noSurveys)


#(3) Test cases for user enrolment
class TestEnrolment(unittest.TestCase):

    def setUp(self):
        db.create_all()
        self.system = SurveySystem()
        self.system.csv_import()

    def test_enrol_user_invalid_courseId(self):
        """
        Enrol user invalid course id
        post: There will be no changes in the database
        """
        print("Enrol user invalid course id")
        u_id = 100
        c_id = 1000

        prev_noEnrolments = len(Enrolment.query.all())
        self.assertEqual(self.system.create_enrolment(u_id, c_id), 0)
        curr_noEnrolments = len(Enrolment.query.all())
        self.assertEqual(prev_noEnrolments, curr_noEnrolments)

    def test_enrol_user_invalid_userId(self):
        """
        Enrol user invalid user id
        post: There will be no changes in the database
        """
        print("Enrol user invalid user id")
        u_id = 9999
        c_id = 1

        prev_noEnrolments = len(Enrolment.query.all())
        self.assertEqual(self.system.create_enrolment(u_id, c_id), 0)
        curr_noEnrolments = len(Enrolment.query.all())
        self.assertEqual(prev_noEnrolments, curr_noEnrolments)

    def test_enrol_valid(self):
        """
        Enrol user valid
        pre : The student isn't already enrolled in the course
        post: The database will have a relationship between
                the course offering and the student
        """
        print("Enrol user valid")
        u_id = 100
        c_id = 2

        prev_noEnrolments = len(Enrolment.query.all())
        self.assertEqual(self.system.create_enrolment(u_id, c_id), 1)
        curr_noEnrolments = len(Enrolment.query.all())
        self.assertEqual(prev_noEnrolments + 1, curr_noEnrolments)


#(4) Test cases for user creation
class TestUserCreation(unittest.TestCase):

    def setUp(self):
        db.create_all()
        self.system = SurveySystem()
        self.system.csv_import()
        self.system.create_user(1, "admin", "password", 3)

    def test_create_user_invalid_username(self):
        """
        Create user invalid username (already taken)
        post: There will be no changes in the database
        """
        print("Create user invalid username (already taken)")
        u_id = 3
        username = "100"
        password = "test9999"
        u_type = 1

        prev_noUsers = len(User.query.all())
        self.assertEqual(self.system.create_user(u_id, username, password, u_type), 0)
        curr_noUsers = len(User.query.all())
        self.assertEqual(prev_noUsers, curr_noUsers)

    def test_create_user_invalid_id(self):
        """
        Create user invalid id (already taken)
        post: There will be no changes in the database
        """
        print("Create user invalid id (already taken)")
        u_id = 100
        username = "newtestuser"
        password = "test9999"
        u_type = 1

        prev_noUsers = len(User.query.all())
        self.assertEqual(self.system.create_user(u_id, username, password, u_type), 0)
        curr_noUsers = len(User.query.all())
        self.assertEqual(prev_noUsers, curr_noUsers)

    def test_create_user_invalid_password(self):
        """
        Create user invalid password (empty)
        post: There will be no changes in the database
        """
        print("Create user invalid password (empty)")
        u_id = 3
        username = "newtestuser"
        password = ""
        u_type = 1

        prev_noUsers = len(User.query.all())
        self.assertEqual(self.system.create_user(u_id, username, password, u_type), 0)
        curr_noUsers = len(User.query.all())
        self.assertEqual(prev_noUsers, curr_noUsers)

    def test_create_user_invalid_type(self):
        """
        Create user invalid type
        post: There will be no changes in the database
        """
        print("Create user invalid type")
        u_id = 3
        username = "newtestuser"
        password = "password"
        u_type = 5

        prev_noUsers = len(User.query.all())
        self.assertEqual(self.system.create_user(u_id, username, password, u_type), 0)
        curr_noUsers = len(User.query.all())
        self.assertEqual(prev_noUsers, curr_noUsers)

    def test_create_user_valid(self):
        """
        Create valid user
        post: New user will be added to database
        """
        print("Create valid user")
        u_id = 2
        username = "newtestuser9999"
        password = "password"
        u_type = 3

        prev_noUsers = len(User.query.all())
        self.assertEqual(self.system.create_user(u_id, username, password, u_type), 1)
        curr_noUsers = len(User.query.all())
        self.assertEqual(prev_noUsers + 1, curr_noUsers)


#(5) Test cases for user Authentication
class TestUserAuthentication(unittest.TestCase):

    def setUp(self):
        db.create_all()
        self.system = SurveySystem()
        self.system.csv_import()
        self.system.create_user(1, "admin", "password", 3)

    def test_authenticate_invalid_username(self):
        """
        Authenticate user invalid username
        post: No user session created
        """
        print("Authenticate user invalid username")
        username = "test9999user"
        password = "password"

        self.assertEqual(self.system.authenticate(username, password), False)

    def test_authenticate_invalid_password(self):
        """
        Authenticate user invalid password (wrong)
        post: No user session created
        """
        print("Authenticate user invalid password (wrong)")
        username = "admin"
        password = "password9999"

        self.assertEqual(self.system.authenticate(username, password), False)


if __name__ == '__main__':
    unittest.main()
    os.remove('pychart.db')
