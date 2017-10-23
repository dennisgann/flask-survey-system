import unittest
from server import db
from dbInteractions import *
from sys_models import SurveySystem

#Test cases for:
#(1) Create Mandatory/Optional Questions
#(2) Create a survey
#(3) Enrol a student 
#(4) Login Authentication
#(5) ???

# Login Authentication
class test_Authentication(unittest.Testcase):
    def setUp(self):
        db.create_all()
        csv_import()

    def test_adminLoginSuccess(self):
        self.assertTrue(authenticate(self, username, password)) #Can't find info in passwords.csv
        self.assertEqual(check_login(self), 3) #Check that the system knows it is an admin

    def test_adminLoginFail(self):
        self.assertFalse(authenticate(self, username, password)) #Can't find info for admin in password.csv

    def test_staffLoginSuccess(self):
        self.assertTrue(authenticate(self, staff670, 50))
        self.assertEqual(check_login(self), 2) #Check that the system knows it is staff

    def test_staffLoginFail(self):
        self.assertFalse(authenticate(self, staff0, -1))

    def test_studentLoginSuccess(self):
        self.assertTrue(authenticate(self, student22, 100))
        self.assertEqual(check_login(self), 1) #Check that the system knows it is a student

    def test_studentLoginFail(self):
        self.assertFalse(authenticate(self, student0, -1))

    def test_guestLoginSuccess(self):
        self.assertTrue(authenticate(self, guest, password)) #Can't find info in passwords.csv

    def test_guestLoginFail(self):
        self.assertTrue(authenticate(self, guest, password))

    def tearDown(self):
        db.session.remove()
        db.drop_all()

#Testing for adding questions to the generic pool
class test_add_question(unittest.Testcase):

    def setUp(self):
        db.create_all()
        csv_import()

    def test_addQuestionMandatorySuccess(self):
        question_name = "valid question"
        type = 1
        required = 1
        #not sure what to do for responses
        self.assertEqual(get_question(question_name),0)
        num_questions = num_question() #function which counts number of questions in database
        add_question(self, question_name, type, required, responses)
        cur_num_questions = num_questions()
        self.assertEqual(num_questions+1, cur_num_questions)
        self.assertNotEqual(get_question(question_name),1) #get_question returns 
        #self.assertTrue(add_question(self, question_name, type, required, responses))

    def test_addQuestionMandatoryFail(self):
        question_name = ""
        type = 1
        required = 1
        responses = ""
        num_questions = num_question()
        with self.assertRaises(InvalidInputException):
            add_question(self,question_name,type,required,responses)
        cur_num_questions = num_questions()
        self.assertEqual(num_questions,cur_num_questions)
        #self.assertFalse(add_question(self, question_name, type, required, responses))

    def test_addQuestionOptionalSuccess(self):
        question_name = "valid question"
        type = 1
        required = 2
        #not sure what to do for responses
        self.assertEqual(get_question(question_name),None)
        num_questions = num_question() #function which counts number of questions in database
        add_question(self, question_name, type, required, responses)
        cur_num_questions = num_questions()
        self.assertEqual(num_questions+1, cur_num_questions)
        self.assertNotEqual(get_question(question_name),None) #get_question returns 
        #self.assertTrue(add_question(self, question_name, type, required, responses))

    def test_addQuestionOptionalFail(self):
        question_name = ""
        type = 1
        required = 2
        responses = ""
        num_questions = num_question()
        with self.assertRaises(InvalidInputException):
            add_question(self,question_name,type,required,responses)
        cur_num_questions = num_questions()
        self.assertEqual(num_questions,cur_num_questions)
        self.assertTrue(add_question(self, question_name, type, required, responses))

    def tearDown(self):
        db.create_all()
        csv_import()

#Test cases for survey creation
class test_add_survey(unittest.Testcase):

    def setUp(self):
        db.create_all()
        csv_import()

    def test_add_survey_success(self):
        survey_name = 'SurveyName'
        survey_id = '3'
        survey_questions = 'questions' #???
        



class test_find_question(unittest.Testcase):
    def test_findQuestionSuccess(self):
        self.assertTrue(find_question(self, 40))

    def test_findQuestionFail(self):
        self.assertFail(find_question(self, -1))

#??? Wait we don't enrol anyone do we 
class TestEnrolment(unittest.Testcase):
    def setUp(self):
        db.create_all()
        csv_import()

    def test_enrolment_student_invalid_course(self):
        zID = 99
        course_offering = ""

        prev_students = num_enrolled_students(course_offering)
        with self.assertRaises(InvalidInputException):
            enrol_user
#??? 

if __name__ == '__main__':
    unittest.main()

#helper functions needed
#num_questions returns no. of questions in database
#get_question returns whether a question is present 1 or not presnt 0 in database 