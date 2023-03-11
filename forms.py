from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

class contactForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email", "type": "email"})
    name = StringField("Name", validators=[DataRequired()], render_kw={"placeholder": "Enter your name"})
    message = TextAreaField("Message", validators=[DataRequired()], render_kw={"placeholder": "Enter your message", "rows" : 8})
    submit = SubmitField("Submit")