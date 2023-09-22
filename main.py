import os
from flask import Flask, render_template, redirect, url_for, flash
from forms import contact_form, login_form, signup_form
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt
# from models import User

path = os.path.abspath(os.getcwd()+"/database/database.db")
app = Flask(__name__)

app.config["SECRET_KEY"] = "12cf392707648385ca40917f"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager  = LoginManager(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

@app.before_first_request
def create_tables(): 
    db.create_all()


@login_manager.user_loader
def load_user(user_id): 
    return User.get(user_id)

@login_manager.unauthorized_handler
def unauthorized(): 
    return redirect(url_for('signup'))


@app.route("/")
def home():
    title = "Home"
    css_file = "base.css"
    return render_template("home.html", title=title, css_file=css_file)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = login_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data): 
            login_user(user)
            flash(f'Login successful')
        else: 
            flash(f'Login failed')
        return redirect(url_for("home"))
    return render_template("login.html", form=form)

@app.route("/logout")
def logout(): 
    logout_user()
    return redirect(url_for("login"))

@app.route("/signup")
def signup():
    form = signup_form()
    if form.validate_on_submit():
        return redirect(url_for("home"))
    return render_template("signup.html", form=form)

@app.route("/about")
def about():
    title = "About Us"
    css_file = "about.css"
    return render_template("about.html", title=title, css_file=css_file)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    title = "Contact Us"
    css_file = "contact.css"
    form = contact_form()
    if form.validate_on_submit():
        flash("THANKS FOR CONTACTING US!")
        return redirect(url_for("contact"))
    return render_template("contact.html", form=form, title=title, css_file=css_file)

@app.route("/recipe")
def recipes():
    title = "Recipes"
    css_file = "recipes.css"
    return render_template("recipes.html", title = title, css_file = css_file)

@app.route('/ingredients')
def ingredients(): 
    title = "Ingredients"
    css_file = "ingredients.css"
    return render_template("ingredients.html", title = title, css_file = css_file)

@app.route('/meal')
def meal(): 
    title = "Meals"
    css_file = "meal.css"
    return render_template("meal.html", title = title, css_file = css_file)

@app.route('/shopping')
def shopping(): 
    title = "Shopping"
    css_file = "shopping.css"
    return render_template("shopping.html", title = title, css_file = css_file)

if __name__ == "__main__":
    app.run(debug=True)