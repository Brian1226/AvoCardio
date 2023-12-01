from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, IntegerField
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

class workout_form(FlaskForm):
    activity = StringField("Enter the workout activity name:", validators=[DataRequired()], render_kw={"placeholder": "Activity"})
    duration = StringField("Enter the duration (mins):", validators=[DataRequired()], render_kw={"placeholder": "Duration"})
    weight = StringField("Enter your weight (lbs):", validators=[DataRequired()], render_kw={"placeholder": "Weight"})
    submit = SubmitField("Submit")
    
class shopping_form(FlaskForm):
    name = StringField("What item are you adding?:", validators=[DataRequired()])
    quantity = IntegerField("How many of them do you want?:", validators=[DataRequired()])
    submit = SubmitField("Add the item!")

class meal_form(FlaskForm):
    name = StringField("Name your meal:")
    save = SubmitField("Save Recipe")