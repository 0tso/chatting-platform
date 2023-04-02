import db
import user

def try_find_user(username):
    with db.Connection() as cur:
        cur.execute("SELECT id FROM Users WHERE name=%s;", (username,))
        if cur.fetchone():
            return True
        else:
            return False