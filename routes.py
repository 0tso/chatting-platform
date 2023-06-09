from functools import wraps
from app import app
import db
from flask import render_template, redirect, request, session
import user
import util
import chat

# Decorator
def requires_login(route_func):
    @wraps(route_func)
    def inner(*args, **kwargs):
        if not user.logged_in():
            return redirect("/login")
        return route_func(*args, **kwargs)
    return inner


@app.route("/")
@requires_login
def index():
    return render_template("index.html", username=user.username(), chat_groups=chat.get_chats())

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
        return {"message": "Invalid login credentials."}, 401

@app.route("/register", methods=["POST"])
def try_register():
    username = request.form["username"]
    password = request.form["password"]

    if (ret := user.is_invalid(username, password)):
        return ret

    if user.try_register(username, password):
        return redirect("/")
    else:
        return {"message": "User already exists."}, 409

@app.route("/logout")
def logout():
    user.logout()
    return redirect("/")

@app.route("/find_user")
@requires_login
def find_user():

    if request.args["csrf_token"] != session["csrf_token"]:
        return {"message": "Invalid csrf_token"}, 403

    username = request.args["username"]
    if username != user.username() and util.try_find_user(username):
        chat_id = chat.create_chat_with_user(username)
        return redirect(f"/chat/{chat_id}")
    else:
        return redirect("/")

@app.route("/chat/<chat_id>")
@requires_login
def open_chat(chat_id):
    if chat.join_chat(chat_id):
        return render_template("chat.html", username=user.username(), users=chat.get_chat_users(chat_id))
    else:
        return {"message": "Unauthorized."}, 401

@app.route("/chat/<chat_id>/hide", methods=["POST"])
@requires_login
def hide_chat(chat_id):

    if request.form["csrf_token"] != session["csrf_token"]:
        return {"message": "Invalid csrf_token"}, 403

    chat.hide_chat(chat_id)
    return redirect("/")