from flask import render_template, url_for, redirect, flash, request
import requests
from urllib.parse import unquote

from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, bcrypt, login_manager, SPOONACULAR_API_KEY
from app.forms import contact_form, login_form, signup_form, add_ingredients
from app.models import User, datetime, load_user, unauthorized, Ingredients


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
    return redirect(url_for("login"))

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



@app.route("/recipe", methods=['GET'])
def recipes():
    title = "Recipes"
    css_file = "recipes.css"
    # user = User.query.filter_by(username=current_user.username().first())
    user = current_user
    ingredients = Ingredients.query.filter_by(user_id = user.id).all()
    # return render_template("recipes.html", title = title, css_file = css_file, ingredients = ingredients)
    return render_template("recipes.html", title = title, css_file = css_file, recipes=[], search_query='')

@app.route("/", methods=['GET', 'POST'])
def getRecipes():
    if request.method == 'POST':
        query = request.form.get('search_query', '')
        recipes = search_recipes(query)
        return render_template('recipes.html', title = title, css_file = css_file, recipes=recipes, search_query=query)
    
    search_query = request.args.get('search-query', '')
    decoded_search_query = unquote(search_query)
    recipes = search_recipes(decoded_search_query)
    return render_template('recipes.html', title = title, css_file = css_file, recipes=recipes, search_query=decoded_search_query)

def search_recipes(query):
    url = f'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': SPOONACULAR_API_KEY,
        'query': query,
        'number': 10,
        'instructionsRequired': True,
        'addRecipeInformation': True,
        'fillIngredients': True,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['results']
    return []

@app.route('/recipe/<int:recipe_id>')
def view_Recipe(recipe_id):
    search_query = request.args.get('search_query', '')
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {
        'apiKey': SPOONACULAR_API_KEY,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        recipe = response.json()
        return render_template('view_recipe.html', recipe=recipe, search_query=search_query)
    return "Recipe not found", 404


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