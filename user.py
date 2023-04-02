from flask import session
import db
from werkzeug.security import check_password_hash, generate_password_hash

def logged_in():
    return "username" in session

def try_login(username, password):
    with db.Connection() as cur:
        cur.execute("SELECT id, password FROM Users WHERE name=%s", (username,))
        user = cur.fetchone()
        if user:
            if check_password_hash(user[1], password):
                session["username"] = username
                session["user_id"] = user[0]
                return True

        return False

def try_register(username, password):
    with db.Connection() as cur:
        cur.execute("SELECT id FROM Users WHERE name=%s", (username,))
        if cur.fetchone():
            return False
        else:
            cur.execute("INSERT INTO Users (name, password) VALUES (%s, %s) RETURNING id", (username, generate_password_hash(password)))
            session["username"] = username
            session["user_id"] = cur.fetchone()[0]
            return True

def logout():
    if "username" in session:
        del session["username"]

def username():
    return session.get("username", None)

def user_id():
    return session.get("user_id", None)