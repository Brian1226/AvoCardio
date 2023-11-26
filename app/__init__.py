import os
from flask import Flask
from urllib.parse import unquote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

path = os.path.abspath(os.getcwd()+"/app/database/database.db")
app = Flask(__name__)

app.config["SECRET_KEY"] = "12cf392707648385ca40917f"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


SPOONACULAR_API_KEY = 'f1c49d83ef6041bb920c6a2d10c70ee8'



login_manager  = LoginManager(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

@app.before_first_request
def create_tables(): 
    db.create_all()

from app import routes, models, forms

if __name__ == '__main__':
    app.run(debug=True)