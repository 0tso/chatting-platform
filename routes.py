from app import app
import db
from flask import render_template, redirect, request
import user

@app.route("/")
def index():
    if user.logged_in():
        return render_template("index.html", username=user.username())
    else:
        return redirect("/login")

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def try_login():
    username = request.form["username"]
    password = request.form["password"]
    if user.try_login(username, password):
        return redirect("/")
    else:
        return redirect("/login")

@app.route("/register", methods=["POST"])
def try_register():
    username = request.form["username"]
    password = request.form["password"]
    if user.try_register(username, password):
        return redirect("/")
    else:
        return redirect("/login")

@app.route("/logout")
def logout():
    user.logout()
    return redirect("/")