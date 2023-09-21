from flask import redirect, url_for
from flask_login import UserMixin
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 

from main import db, login_manager, app
from datetime import datetime, date

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable = False)
    email = db.Column(db.String(100), unique=True, nullable = False)
    pfp = db.Column(db.String(255), nullable = False, default='default.jpg')
    password = db.Column(db.String(255), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())

    @staticmethod 
    def verify_token(token):
        pass

    def check_user(self, username): 
        if username != self.username: 
            return False
        return True

    def __repr__(self): 
        return f'{self.id}' \
            f': {self.username} ' \
            f': {self.email} ' \
            f': {self.data_created.strftime("%d/%m/%Y, %H:%M:%S")}'