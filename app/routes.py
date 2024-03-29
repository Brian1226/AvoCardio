from app import app, db, bcrypt, login_manager, mail
from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import contact_form, login_form, signup_form, workout_form, shopping_form, meal_form
from app.models import User, datetime, load_user, unauthorized, ShoppingList, Recipes
import requests, string
from urllib.parse import unquote
from flask_mail import Message
import os
from dotenv import load_dotenv

load_dotenv()

SPOONACULAR_API_KEY = os.environ.get('SPOONACULAR_API_KEY')
WORKOUT_API_KEY = os.environ.get('WORKOUT_API_KEY')

@app.route("/")
def index():
    title = "Home"
    css_file = "base.css"
    return render_template("index.html", title=title, css_file=css_file)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = login_form()
    if form.validate_on_submit():
        email = User.query.filter_by(email=form.email.data).first()
        user = User.query.filter_by(username=form.username.data).first()
        if user and email and bcrypt.check_password_hash(user.password, form.password.data): 
            login_user(user)
            flash(f"Login successful!")
            return redirect(url_for("index"))
        else: 
            flash(f"Login failed!")
            return redirect(url_for("login"))
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout(): 
    logout_user()
    flash("Log out successful!")
    return redirect(url_for("index"))

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
            flash("Sign up successful!")
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
        flash("Thanks for contacting us!")
        message_subject = f"AvoCardio Email from {form.name.data}"
        message = Message(message_subject, sender=form.email.data, recipients=['testuseremail2024@gmail.com'])
        message.body = form.message.data
        mail.send(message)
        return redirect(url_for("contact"))
    return render_template("contact.html", form=form, title=title, css_file=css_file)

@app.route("/recipe")
@login_required
def recipes():
    title = "Recipes"
    css_file = "recipes.css"
    return render_template("recipes.html", title = title, css_file = css_file, recipes=[], search_query='')

@app.route("/recipe", methods=['GET', 'POST'])
def getRecipes():
    title = "Recipes"
    css_file = "recipes.css"
    if request.method == 'POST':
        query = request.form.get('search_query', '')
        recipes = search_recipes(query)
        return render_template('recipes.html', title = title, css_file = css_file, recipes=recipes, search_query=query)

    search_query = request.args.get('search_query', '')
    decoded_search_query = unquote(search_query)
    recipes = search_recipes(decoded_search_query)
    return render_template('recipes.html', title = title, css_file = css_file, recipes=recipes, search_query=decoded_search_query)

def search_recipes(query):
    url = f'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': SPOONACULAR_API_KEY,
        'query': query,
        'number': 60,
        'instructionsRequired': True,
        'addRecipeInformation': True,
        'fillIngredients': True,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['results']
    return []

@app.route('/recipe/<int:recipe_id>', methods=['GET', 'POST'])
def view_Recipe(recipe_id):
    form = meal_form()
    search_query = request.args.get('search_query', '')
    url = f'https://api.spoonacular.com/recipes/{recipe_id}/information'
    params = {
        'apiKey': SPOONACULAR_API_KEY,
    }
    
    response = requests.get(url, params=params)
    recipe = response.json()
    
    if form.validate_on_submit():
        newrecipe = Recipes(api_key=recipe_id, user_id=current_user.id)
        db.session.add(newrecipe)
        for ingredient in recipe['extendedIngredients']:
            newitem = ShoppingList(user_id=current_user.id, name=string.capwords(ingredient['name']), quantity=string.capwords(str(ingredient['measures']['us']['amount'])+ " " + ingredient['measures']['us']['unitLong']), recipe_name=string.capwords(recipe['title']))
            db.session.add(newitem)
        db.session.commit()
        flash("Recipe saved!")

    if response.status_code == 200:
        return render_template('view_recipe.html', recipe=recipe, search_query=search_query, form=form)
    return "Recipe not found", 404    

@app.route('/meal')
@login_required
def meal(): 
    title = "Meals"
    css_file = "meal.css"
    recipes = Recipes.query.filter_by(user_id=current_user.id).all()
    meals = []
    for i in range(0, len(recipes)):
        url = f'https://api.spoonacular.com/recipes/{recipes[i].api_key}/information'
        params = {
            'apiKey': SPOONACULAR_API_KEY,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            meals.append(response.json())
    return render_template("meal.html", title = title, css_file = css_file, meals = meals)

@app.route('/meal/<int:meal_id>')
@login_required
def view_meal(meal_id):
    url = f'https://api.spoonacular.com/recipes/{meal_id}/information'
    params = {
        'apiKey': SPOONACULAR_API_KEY,
    }
    css_file = "recipes.css"
    meal = request.args.get('meal', '')
    response = requests.get(url, params=params)
    if response.status_code == 200:
        meal = response.json()
        return render_template('view_meal.html', meal=meal)
    return "Recipe not found", 404 

@app.route('/deleteMeal/<int:meal_id>', methods=["GET", "POST"])
@login_required
def deleteMeal(meal_id): 
    recipe = Recipes.query.filter_by(api_key=meal_id, user_id=current_user.id).first()
    if recipe.user_id != current_user.id:  
        flash('You do not have access to that recipe!')
        return redirect(url_for('index'))
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('meal'))

@app.route('/shopping')
@login_required
def shopping(): 
    title = "Shopping"
    css_file = "shopping.css"
    shop = ShoppingList.query.filter_by(user_id=current_user.id).all()
    return render_template("shopping.html", title = title, css_file = css_file, shoplist = shop) 

@app.route('/addShoppingItem', methods=["GET", "POST"])
@login_required
def addItem(): 
    print(current_user.id)
    title = "Add shopping item"
    css_file = 'shopping.css' 
    form = shopping_form()
    shoplist = ShoppingList.query.filter_by(user_id=current_user.id).all()
    if form.validate_on_submit(): 
        itemname = request.form["name"]
        itemquantity = request.form["quantity"]
        item = ShoppingList(user_id=current_user.id, name=itemname, quantity=itemquantity) 
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('shopping'))
    return render_template("additem.html", title = title, css_file = css_file, form=form, shoplist=shoplist)

@app.route('/updateQuan/<int:itemnumber>', methods=["GET", "POST"])
@login_required
def updateQuan(itemnumber): 
    item = ShoppingList.query.get_or_404(itemnumber) 
    if item.user_id != current_user.id: 
        return redirect(url_for('index'))
    
    if request.method == 'POST': 
        item.name = request.form['name']
        item.quantity = request.form['quantity']
        item.recipe_name = request.form['recipe'] 
        db.session.commit() 
        return redirect(url_for('shopping'))
            
        
    else: 
        return render_template("upQuan.html", title = "Update Item Quantity", css_file = 'shopping.css', item=item)

@app.route('/deleteItem/<int:itemnumber>', methods=["GET", "POST"])
@login_required
def deleteItem(itemnumber): 
    item = ShoppingList.query.get_or_404(itemnumber)
    if item.user_id != current_user.id: 
        return redirect(url_for('index'))
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('shopping'))

@app.route('/deleteAll')
@login_required 
def deleteAll(): 
    items = ShoppingList.query.filter_by(user_id=current_user.id).all()
    for item in items: 
        db.session.delete(item)
    db.session.commit()
    return redirect(url_for('shopping'))

@app.route('/workout', methods=["GET", "POST"])
@login_required
def workout(): 
    title = "Workout Plan"
    css_file = "workout.css"
    form = workout_form()
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

            data_list.append ({
                "name": name,
                "calories_per_hour": calories_per_hour,
                "duration_minutes": duration_minutes,
                "total_calories": total_calories
            })
        return data_list
    else:
        return f"Error: {response.status_code} -> {response.text}"
