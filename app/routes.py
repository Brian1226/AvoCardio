from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, bcrypt, login_manager
from app.forms import contact_form, login_form, signup_form, workout_form
from app.models import User, datetime, load_user, unauthorized, Ingredients
import requests
import json

@app.route("/")
def home():
    title = "Home"
    css_file = "base.css"
    return render_template("home.html", title=title, css_file=css_file)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = login_form()
    if form.validate_on_submit():
        email = User.query.filter_by(email=form.email.data).first()
        user = User.query.filter_by(username=form.username.data).first()
        if user and email and bcrypt.check_password_hash(user.password, form.password.data): 
            login_user(user)
            flash(f"Login successful")
            return redirect(url_for("home"))
        else: 
            flash(f"Login failed")
            return redirect(url_for("login"))
    return render_template("login.html", form=form)

@app.route("/logout")
def logout(): 
    logout_user()
    return redirect(url_for("home"))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = signup_form()
    if form.validate_on_submit():
        existing_username = User.query.filter_by(username=form.username.data).first()
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash("Sign up failed. Email already exists.")
            return redirect(url_for("signup"))
        elif existing_username:
            flash("Sign up failed. Username already exists.")
            return redirect(url_for("signup"))
        else:
            user = User(
                email=form.email.data, 
                username=form.username.data, 
                password=bcrypt.generate_password_hash(form.password.data).decode("utf-8"), 
                date_created=datetime.utcnow())
            db.session.add(user)
            db.session.commit()
            flash("Sign up successful")
            return redirect(url_for("login"))
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
    # user = User.query.filter_by(username=current_user.username().first())
    user = current_user
    ingredients = Ingredients.query.filter_by(user_id = user.id).all()
    return render_template("recipes.html", title = title, css_file = css_file, ingredients = ingredients)

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

@app.route('/workout', methods=["GET", "POST"])
def workout(): 
    title = "Workout Plan"
    css_file = "workout.css"
    form = workout_form()
    WORKOUT_API_KEY = "TPX1b3+XQpDjzWCQFqt8iQ==JGmx4LEDsN1puAQh"
    result = []
    
    if form.validate_on_submit():
        activity = request.form["activity"]
        duration = request.form["duration"]
        weight = request.form["weight"]
        url = 'https://api.api-ninjas.com/v1/caloriesburned?activity={}&weight={}&duration={}'.format(activity,weight,duration)
        result = calories_burned(WORKOUT_API_KEY, url)

    return render_template("workout.html", title = title, css_file = css_file, form=form, result=result)

def calories_burned(WORKOUT_API_KEY, url):
    response = requests.get(url, headers={'X-Api-Key': WORKOUT_API_KEY})
    
    if response.status_code == requests.codes.ok:
        response_list = response.json()
        data_list = []

        for data in response_list:
            name = data.get("name", "")
            calories_per_hour = data.get("calories_per_hour", "")
            duration_minutes = data.get("duration_minutes", "")
            total_calories = data.get("total_calories", "")
            # duration_minutes = float(duration)
            # total_calories = calories_per_hour * (duration_minutes / 60)

            data_list.append ({
                "name": name,
                "calories_per_hour": calories_per_hour,
                "duration_minutes": duration_minutes,
                "total_calories": total_calories
            })
        return data_list
    else:
        return f"Error: {response.status_code} -> {response.text}"