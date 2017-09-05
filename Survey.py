import csv

class Survey:
    def __init__(self, sid, state, name, course, questions):
        self._id = sid
        self._name = name
        self._course = course
        self._questions = questions
        self._state = state

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self,sid):
        self._id = id

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

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self,state):
        self._state = state


    ##functions

    def write(self):

        with open('surveys/' +  self._id + '.csv','w') as csv_out:
            writer = csv.writer(csv_out)
            writer.writerow([self._id, self._name, self._course])
            writer.writerow(self._questions)

        with open('surveys.csv','a') as csv_out:
            writer = csv.writer(csv_out)
            writer.writerow([self._id, self._state, self._name, self._course])

            return 1 ##success

        return 0 ##failure
