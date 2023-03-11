from flask import Flask, render_template, session, redirect, url_for, flash
from forms import contactForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "mykey"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = contactForm()
    if form.validate_on_submit():
        flash("THANKS FOR CONTACTING US!")
        session["email"] = form.email.data
        session["name"] = form.name.data
        session["message"] = form.message.data
        return redirect(url_for("contact"))
    return render_template("contact.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
