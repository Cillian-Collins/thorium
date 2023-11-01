from flask import Flask, render_template
from db import setup_database, fetch_exploits
import threading
import sqlite3

app = Flask(__name__)
conn = setup_database()


@app.route('/')
def dashboard():
    return render_template("dashboard.html")


@app.route('/submissions')
def submissions():
    return render_template("submissions.html")


@app.route('/services')
def services():
    return render_template("services.html")


@app.route('/exploits')
def exploits():
    local = threading.local()

    if not hasattr(local, "conn"):
        local.conn = sqlite3.connect('database.db')

    items = fetch_exploits()
    return render_template("exploits.html", exploits=items)


@app.route('/exploits/add')
def add_exploit():
    return render_template("add_exploit.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)