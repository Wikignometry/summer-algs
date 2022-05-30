from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "hello" # for session
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # to silence warnings
app.permanent_session_lifetime = timedelta(minutes=5) # for session

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True  # <--- makes the permanent session
        user = request.form["nm"]
        session["user"] = user
        foundUser =  users.query.filter_by(name=user).first() # returns first user matching name
        if foundUser:
            session["email"]= foundUser.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit() # must commit every time you add (because you can reverse)

        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash(f"Already logged in!", "info")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())

@app.route("/user", methods=["POST", "GET"])
def user():
    if "user" in session:
        email = None
        user = session["user"]
        if request.method == 'POST':
            email = request.form["email"]
            session['email'] = email
            foundUser =  users.query.filter_by(name=user).first()
            foundUser.email = email
            db.session.commit()
            flash("Email was saved!")
        else:
            if "email" in session:
                email = session['email']


        return render_template("user.html", email=email)
    else:
        flash(f"You are not logged in!", "info")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out, {user}", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    db.create_all() # above app.run
    app.run(debug=False)
