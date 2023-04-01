from app import app
import db
from flask import render_template

@app.route("/")
def index():
    with db.Connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM Users;")
        vals = cur.fetchall()
        return render_template("index.html", users=vals)