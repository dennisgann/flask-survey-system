import csv

class Question:
    def __init__(self,qid,state,text,responses):
        self._text = text
        self._id = qid
        self._state = state
        self._responses = responses

    ##properties

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self,text):
        self._text = text

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self,id):
        self._id = id

    @property
    def responses(self):
        return self._responses

    @responses.setter
    def responses(self,responses):
        self._responses = responses

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self,state):
        self._state = state


    ##functions

    def write(self):
        with open('questions.csv','a') as csv_out:
            writer = csv.writer(csv_out)
            writer.writerow([self._id, self._state, self._text] + self._responses)

            return 1 ##success

        return 0 ##failure
