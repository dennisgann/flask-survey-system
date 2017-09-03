class Question:
    def __init__(self,text,id):
        self._text = text
        self._id = id

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self,text):
        self._text = text

    @property
    def id(self):
        return self._id

    #@text.writer
    def writer(self,text,id):
        with open('questions.csv','w') as csv_out:
            writer=csv.writer(csv_out)
            for row in writer:
                writer.writerow(self._id,self._text)

            return "Question has been successfully added."
