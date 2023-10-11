import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

path = os.path.abspath(os.getcwd()+"/database/database.db")
app = Flask(__name__)

app.config["SECRET_KEY"] = "mykey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ '/home/tng/AvoCardio/app/database/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager  = LoginManager(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

@app.before_first_request
def create_tables(): 
    db.create_all()

from app import routes, models, forms