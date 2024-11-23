from flask import Flask
import psycopg2
from dotenv import load_dotenv
import os
from models import db, User, Dataset, File

load_dotenv()

url = os.getenv('DATABASE_URL')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

connection = psycopg2.connect(url)

app.route('/')
def hello_world():
    return 'Hello World!'


