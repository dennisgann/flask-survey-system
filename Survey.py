class Survey:
    def __init__(self, id, name, course, questions):
        self._id = id
        self._name = name
        self._course = course
        self._questions = questions

    @property
    def id(self):
        return self._id

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

    #Writes to survey.csv, mostly taken from def createSurvey():
    def creator(self):

        #with open('survey.csv','w') as csv_out:
        #    writer=csv.writer(csv_out)
        #    for row in writer:
        #        writer.writerow(self.id,self.name,self.course)
        #           for row in writer:

        with open('surveys/' + id + '.csv','w') as csv_out:
            writer = csv.writer(csv_out)
            writer.writerow([self._name, self._course])
            writer.writerow(self._questions)

        with open('surveys.csv','a') as csv_out:
            writer = csv.writer(csv_out)
            writer.writerow([self._id, self._name, self._course, 1])

        return "Successfully created survey with ID: " + self._id

        questions = []
        with open('questions.csv','r') as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                questions.append(row)
                # I'm not sure how the program knows which    questions are needed

        course = []

        with open('courses.csv','r') as csv_in:
        reader = csv.reader(csv_in)
        next(reader)
        for row in reader:
            if row:
                courses.append(row)

        return render_template("createSurvey.html", questions=questions, courses=courses)
