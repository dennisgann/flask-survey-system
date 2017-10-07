import csv, os, ast
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from server import db

class SurveySystem():

    def add_question(self, q_text, type, required, responses):
        newQ = Question(text=q_text, state=1, type=type, required=required, responses=str(responses))
        db.session.add(newQ)
        db.session.commit()
        return 1 #success

    #??? required
    def find_question(q_id):
        question = Question.query.filter_by(id=q_id).first()
        return question

    def update_question(self, q_id, q_text, state, type, required, responses):
        question = Question.query.filter_by(id=q_id).first()
        question.text = q_text
        question.state = state
        question.type = type
        question.required = required
        question.responses = str(responses)
        db.session.commit()
        return 1


    def create_survey(self, name, c_id, questions):
        newS = Survey(name=name, c_id=c_id, state=1, type=type, questions=str(questions))
        db.session.add(newS)
        db.session.commit()
        return 1 #success

    def update_survey(self, s_id, q_text, state, type, required, responses):
        question = Question.query.filter_by(id=q_id).first()
        question.text = q_text
        question.state = state
        question.type = type
        question.required = required
        question.responses = str(responses)
        db.session.commit()
        return 1

    def csv_import(self):

        if not (os.path.isfile("data/courses.csv") and \
        os.path.isfile("data/enrolments.csv") and \
        os.path.isfile("data/passwords.csv")):
            return 0 #failure

        with open('data/courses.csv','r') as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                if not Course.query.filter_by(course=row[0], session=row[1]).first():
                    course = Course(course=row[0], session=row[1])
                    db.session.add(course)

            db.session.commit()


        with open('data/enrolments.csv','r') as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                c_id = Course.query.filter_by(course=row[1], session=row[2]).first().id
                if not c_id:
                    return 0 #failure

                if not Enrolment.query.filter_by(u_id=row[0], c_id=c_id).first():
                    enrolment = Enrolment(u_id=row[0], c_id=c_id)
                    db.session.add(enrolment)

            db.session.commit()

        with open('data/passwords.csv','r') as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                u_type = 0
                if row[2] == "student":
                    u_type = 1
                elif row[2] == "staff":
                    u_type = 2

                if not User.query.filter_by(id=row[0]).first() and u_type:
                    user = User(id=row[0], username=row[0], password=generate_password_hash(row[1]), type=u_type)
                    db.session.add(user)

            db.session.commit()

        return 1 #success


    def authenticate(self, user_name, password):
        user = User.query.filter_by(username=str.lower(user_name)).first()

        if not user:
            return False

        if check_password_hash(user.password, password):
            session['logged_in'] = True
            session['username'] = user.username
            session['user_id'] = user.id
            session['user_type'] = user.type
            return True #valid user

        return False #credentials incorrect

    def check_login(self):
        if session.get('user_type'):
                return session['user_type']
        else:
            return 0



    def add_user(self, id, name, password):
        session = self.DBSession()
        user = User(id=id, name=name, password=password)
        self.add_row(session, user)

    def post_item(self, owner_id, item_id, name, desc):
        seller = self.query_user(owner_id)
        session = self.DBSession()
        item = Item(id=item_id, name=name, desc=desc, seller_id=owner_id, seller=seller)
        self.add_row(session, item)

    def make_bid(self, bid_id, user_id, item_id, price):
        user = self.query_user(user_id)
        item = self.query_item(item_id)
        session = self.DBSession()
        bid = Bid(id=bid_id, bidder_id=user_id, item_id=item_id, bidder=user, item=item,price=price)
        self.add_row(session, bid)

    def query_item(self, item_id):
        session = self.DBSession()
        item = session.query(Item).filter(Item.id == item_id).one()
        session.close()
        return item

    def query_user(self, user_id):
        session = self.DBSession()
        user = session.query(User).filter(User.id == user_id).one()
        session.close()
        if user is not None:
            return user
        else: return None

    def add_row(self, session, row):
        session.add(row)
        session.commit()
        session.close()

    def get_items(self, item_id):
        item = self.query_item(item_id)
        seller = self.query_user(item.seller_id)
        if item is not None:
            print("Item name: " + item.name + ", Description: " + item.desc + ", Seller: " + seller.name + "\n")
        else:
            return None

    def get_user(self, user_id):
        user = self.query_user(user_id)
        if user is None:
            print("User not found!")
        else:
            print("User name: " + user.name + ", Password: " + user.password + "\n")

    def search_posts(self, user_id):
        user = self.query_user(user_id)
        session = self.DBSession()
        items = session.query(Item).filter(Item.seller == user)
        session.close()
        print(user.name + "'s Post: ")
        for item in items:
            print("Item: " + item.name + ", Description: " + item.desc)
        print()

    def search_user_bids(self, user_id):
        user = self.query_user(user_id)
        session = self.DBSession()
        bids = session.query(Bid).filter(Bid.bidder == user)
        print(user.name + "'s Bids: ")
        for bid in bids:
            print("item: " + bid.item.name + ", bidder: " + bid.bidder.name + ", price " +str(bid.price))
        print()

    def search_item_bids(self, item_id):
        item = self.query_item(item_id)
        session = self.DBSession()
        bids = session.query(Bid).filter(Bid.item == item)
        print(item.name + "'s Bids: ")
        for bid in bids:
            print("item: " + bid.item.name + ", bidder: " + bid.bidder.name + ", price " + str(bid.price))
        print()


class User(db.Model):

    __tablename__ = 'USERS'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Integer, nullable=False)

class Course(db.Model):

    __tablename__ = 'COURSES'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    course = db.Column(db.String(10), nullable=False)
    session = db.Column(db.String(5), nullable=False)

class Enrolment(db.Model):

    __tablename__ = 'ENROLMENTS'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    u_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    c_id = db.Column(db.Integer, db.ForeignKey(Course.id), nullable=False)
    user = db.relationship(User)
    course = db.relationship(Course)

class Question(db.Model):

    __tablename__ = 'QUESTIONS'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    text = db.Column(db.Text, nullable=False)
    state = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    required = db.Column(db.Integer, nullable=False)
    responses = db.Column(db.Text, nullable=False)

    def responsesList(self):
         return ast.literal_eval(self.responses)

class Survey(db.Model):

    __tablename__ = 'SURVEYS'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    c_id = db.Column(db.Integer, db.ForeignKey(Course.id), nullable=False)
    state = db.Column(db.Integer, nullable=False)
    questions = db.Column(db.Text, nullable=False)
    course = db.relationship(Course)

    def questionsList(self):
         return ast.literal_eval(self.questions)

class Response(db.Model):

    __tablename__ = 'RESPONSES'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    u_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    s_id = db.Column(db.Integer, db.ForeignKey(Survey.id), nullable=False)
    responses = db.Column(db.Text, nullable=False)
    user = db.relationship(User)
    survey = db.relationship(Survey)

    def responsesList(self):
         return ast.literal_eval(self.responses)
