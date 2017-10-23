from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.secret_key = "#FFDGCL2017!!#"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pychart.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
