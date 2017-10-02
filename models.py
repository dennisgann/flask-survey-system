##pyChart - UNSW COMP1531 17s2 Group Project
##Created by Frank Foo, Dennis Gann and Charmaine Leung

from abc import abstractmethod
import csv
import sqlite3


#abstract object class
class Object():

    def __init__(self, oid, state):
        self._id = oid
        self._state = state

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self,oid):
        self._id = oid

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self,state):
        self._state = state


#abstract object store class
class ObjectStore():

    def __init__(self):
        self._data = []
        self.load()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self,data):
        self._data = data

    @property
    def active(self):
        active = []
        for obj in self._data:
            if obj.state == '1':
                active.append(obj)
        return active

    @property
    def inactive(self):
        inactive = []
        for obj in self._data:
            if obj.state == '0':
                inactive.append(obj)
        return inactive

    #adds an object to the store
    def add(self,dataObject):
        self._data.append(dataObject)
        if self.save():
            return 1 #success
        else:
            return 0 #failure

    #update an object in the store
    def update(self,dataObject):
        for i in range(0, len(self._data)):
            if dataObject.id == self._data[i].id:
                self._data[i] = dataObject
                self.save()
                return 1 #sucess

        return 0 #no object exists with mathching id

    #finds an object in store with matching id, returns object
    def find(self,objectID):
        for obj in self._data:
            if objectID == obj.id:
                return obj #sucess returns object

        return 0 #failure no object exists with given id

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self):
        pass


#question object class, extends object
class Question(Object):

    #constructor
    def __init__(self,qid,state,text,responses):
        Object.__init__(self, qid, state)
        self._text = text
        self._responses = responses

    ##properties
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self,text):
        self._text = text

    @property
    def responses(self):
        return self._responses

    @responses.setter
    def responses(self,responses):
        self._responses = responses


#survey object class, extends object
class Survey(Object):

    #constructor
    def __init__(self, sid, state, name, course, questions):
        Object.__init__(self, sid, state)
        self._name = name
        self._course = course
        self._questions = questions

    ##properties
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

#user class
class User:
    
    #constructor
    def __init__(self,zid, name, password):
        self._zid = zid
        self._name = name
        self._password = password
        
    ##properties
    @property
    def zid(self):
        return self._zid

    @zid.setter
    def zid(self,zid):
        self._zid = zid
        
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,name):
        self._name = name
    
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,password):
        self._password = password      
          
#admin subclass
class Admin(User):
    pass

#staff subclass
class Staff(User):
    
    #constructor
    def __init__(self, zid, name, password, course, semester):
        super().__init__(zid, name, password)
        self._course = course
        self._semester = semester
    
    ##properties
    @property
    def course(self):
        return self._course

    @course.setter
    def course(self,course):
        self._course = course
    
    @property
    def semester(self):
        return self._semester

    @semester.setter
    def semester(self,semester):
        self._semester = semester
        
#student subclass
class Student(User):

    #constructor
    def __init__(self, id, name, password, course, semester):
        super().__init__(zid, name, password)
        self._course = course
        self._semester = semester

    ##properties
    @property
    def course(self):
        return self._course

    @course.setter
    def course(self,course):
        self._course = course
    
    @property
    def semester(self):
        return self._semester

    @semester.setter
    def semester(self,semester):
        self._semester = semester

#saving questions

def save_question(question):

    conn = sqlite3.connect('pychart.db')
    c = conn.cursor()
    c.execute("INSERT INTO questions VALUES (?,?,?,?)", (question.qid, question.state, question.text, question.responses))  
    
    conn.commit()
    conn.close()  

#saving surveys

def save_survey(survey):

    conn = sqlite3.connect('pychart.db')
    c = conn.cursor()
    c.execute("INSERT INTO surveys VALUES (?,?,?,?,?)", (survey.sid, survey.state, survey.name, survey.course, survey.questions)) 
    
    conn.commit()
    conn.close()   

#saving staff

def save_staff(staff):

    conn = sqlite3.connect('pychart.db')
    c = conn.cursor()
    c.execute("INSERT INTO staff VALUES (?,?,?,?,?)", (staff.zid, staff.name, staff.password, staff.course, staff.semester)) 
    
    conn.commit()
    conn.close()  
    
#saving students

def save_student(student):

    conn = sqlite3.connect('pychart.db')
    c = conn.cursor()
    c.execute("INSERT INTO student VALUES (?,?,?,?,?)", (student.zid, student.name, student.password, student.course, student.semester)) 
    
    conn.commit()
    conn.close()  
