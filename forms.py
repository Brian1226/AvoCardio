from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

class contact_form(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email", "type": "email"})
    name = StringField("Name", validators=[DataRequired()], render_kw={"placeholder": "Enter your name"})
    message = TextAreaField("Message", validators=[DataRequired()], render_kw={"placeholder": "Enter your message", "rows" : 8})
    submit = SubmitField("Submit")

class login_form(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email", "type": "email"})
    username = StringField("Username", validators=[DataRequired()], render_kw={"placeholder": "Enter your username"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Enter your password"})
    login = SubmitField("Log In")

class signup_form(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email", "type": "email"})
    username = StringField("Username", validators=[DataRequired()], render_kw={"placeholder": "Enter your username"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Enter your password"})
    signup = SubmitField("Sign Up")