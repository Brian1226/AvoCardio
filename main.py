from flask import Flask, render_template, session, redirect, url_for, flash
from forms import contactForm, loginForm, signupForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "mykey"

@app.route("/")
def home():
    title = "Home"
    return render_template("home.html", title=title)

@app.route("/login")
def login():
    form = loginForm()
    if form.validate_on_submit():
        return redirect(url_for("home"))
    return render_template("login.html", form=form)

@app.route("/signup")
def signup():
    form = signupForm()
    if form.validate_on_submit():
        return redirect(url_for("home"))
    return render_template("signup.html", form=form)

@app.route("/about")
def about():
    title = "About Us"
    return render_template("about.html", title=title)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    title = "Contact Us"
    form = contactForm()
    if form.validate_on_submit():
        flash("THANKS FOR CONTACTING US!")
        return redirect(url_for("contact"))
    return render_template("contact.html", form=form, title=title)

if __name__ == "__main__":
    app.run(debug=True)
