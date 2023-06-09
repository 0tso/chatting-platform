import secrets
from flask import session
import db
from werkzeug.security import check_password_hash, generate_password_hash

MAX_USERNAME_LENGTH = 20

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
                session["csrf_token"] = secrets.token_hex(16)
                return True

        return False

def is_invalid(username, password):
    if len(username) > MAX_USERNAME_LENGTH:
        return {"message": f"Username too long. Maximum length is {MAX_USERNAME_LENGTH}."}, 413

    return False

def try_register(username, password):
    with db.Connection() as cur:
        cur.execute("SELECT id FROM Users WHERE name=%s", (username,))
        if cur.fetchone():
            return False
        else:
            cur.execute("INSERT INTO Users (name, password) VALUES (%s, %s) RETURNING id", (username, generate_password_hash(password)))
            user_id = int(cur.fetchone()[0])
            cur.execute("INSERT INTO ChatGroups (user_id, name, index) VALUES (%s, 'Active chats', 0)", (user_id, ))
            session["username"] = username
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)
            return True

def logout():
    if "username" in session:
        del session["username"]

def username():
    return session.get("username", None)

def user_id():
    return session.get("user_id", None)