from flask import Flask, render_template, redirect, url_for, flash
from forms import contact_form, login_form, signup_form

app = Flask(__name__)

app.config["SECRET_KEY"] = "mykey"

@app.route("/")
def home():
    title = "Home"
    css_file = "base.css"
    return render_template("home.html", title=title, css_file=css_file)

@app.route("/login")
def login():
    form = login_form()
    if form.validate_on_submit():
        return redirect(url_for("home"))
    return render_template("login.html", form=form)

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

if __name__ == "__main__":
    app.run(debug=True)
