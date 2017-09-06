from abc import abstractmethod
import csv

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


class Question(Object):
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



class Survey(Object):
    def __init__(self, sid, state, name, course, questions):
        Object.__init__(self, sid, state)
        self._name = name
        self._course = course
        self._questions = questions

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



class QuestionStore(ObjectStore):

    def __init__(self):
        ObjectStore.__init__(self)

    def load(self):
        del self._data[:] #clears list

        with open('data/questions.csv','r') as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                question = Question(row[0], row[1], row[2], row[3:])
                self._data.append(question)

            return 1 #success

        return 0 #failure


    def save(self):
        with open('data/questions.csv','w') as csv_out:
            writer = csv.writer(csv_out)
            for question in self._data:
                writer.writerow([question.id, question.state, question.text] + question.responses)

            return 1 #success

        return 0 #failure


class SurveyStore(ObjectStore):

    def __init__(self):
        ObjectStore.__init__(self)

    def load(self):
        del self._data[:] #clears list

        with open('data/surveys.csv','r') as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                survey = Survey(row[0], row[1], row[2], row[3], row[4:])
                self._data.append(survey)

            return 1 #success

        return 0 #failure


    def save(self):
        with open('data/surveys.csv','w') as csv_out:
            writer = csv.writer(csv_out)
            for survey in self._data:
                writer.writerow([survey.id, survey.state, survey.name, survey.course] + survey.questions)

            return 1 #success

        return 0 #failure
