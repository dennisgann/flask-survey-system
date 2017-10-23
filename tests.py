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


#helper functions needed
#num_questions() returns no. of questions in database
#get_question() returns whether a question is present 1 or not present 0 in database 
#num_surveys() returns no. of surveys in database 

# Login Authentication
class test_Authentication(unittest.Testcase):
    def setUp(self):
        db.create_all()
        csv_import()

    def test_adminLoginSuccess(self):
        username = admin
        password = password
        self.assertTrue(authenticate(self, username, password)) 
        self.assertEqual(check_login(self), 3) #Check that the system knows it is an admin

    def test_adminLoginFail(self):
        username = john
        password = smith
        self.assertFalse(authenticate(self, username, password))

    def test_staffLoginSuccess(self):
        username = 80
        password = staff880
        self.assertTrue(authenticate(self, username, password))
        self.assertEqual(check_login(self), 2) #Check that the system knows it is staff

    def test_staffLoginFail(self):
        username = john
        password = smith
        self.assertFalse(authenticate(self, username, password))

    def test_studentLoginSuccess(self):
        username = 100
        password = student228
        self.assertTrue(authenticate(self, useranem, password))
        self.assertEqual(check_login(self), 1) #Check that the system knows it is a student

    def test_studentLoginFail(self):
        username = john
        password = smith
        self.assertFalse(authenticate(self, username, smith))

    def test_guestLoginSuccess(self):
        username = guest #??
        password = password #?? 
        self.assertTrue(authenticate(self, username, password)) 

    def test_guestLoginFail(self):
        username = john
        password = smith
        self.assertTrue(authenticate(self, username, password))

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
        responses = 'responses' #not sure what to do for responses
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
        responses = 'responses' #not sure what to do for responses
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
class test_create_survey(unittest.Testcase):

    def setUp(self):
        db.create_all()
        csv_import()

    def test_create_survey_success(self):
        survey_name = 'SurveyName'
        survey_id = '3'
        survey_questions = 'questions' #???
        num_surveys = num_surveys()
        create_survey(self, survey_name, survey_id, survey_questions)
        cur_num_surveys = num_surveys()
        self.assertEqual(num_surveys+1,cur_num_surveys)

    def test_create_survey_fail(self):
        survey_name = ""
        survey_id = '2'
        survey_questions = ""
        num_surveys = num_surveys()
        with self.assertRaises(InvalidInputException):
            create_survey(self, survey_name, survey_id, survey_questions)
        cur_num_surveys = num_surveys()
        self.assertEqual(num_surveys,cur_num_surveys)


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