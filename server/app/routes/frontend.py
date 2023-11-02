from app.db import fetch_exploits, fetch_submissions
from flask import Blueprint, render_template
import sqlite3
import threading


frontend = Blueprint("frontend", __name__)


@frontend.route('/')
def dashboard():
    return render_template("dashboard.html")


@frontend.route('/submissions')
def submissions():
    local = threading.local()

    if not hasattr(local, "conn"):
        local.conn = sqlite3.connect('/database/database.db')

    items = fetch_submissions()
    return render_template("submissions.html", submissions=items)


@frontend.route('/services')
def services():
    return render_template("services.html")


@frontend.route('/exploits')
def exploits():
    local = threading.local()

    if not hasattr(local, "conn"):
        local.conn = sqlite3.connect('/database/database.db')

    items = fetch_exploits()
    return render_template("exploits.html", exploits=items)


@frontend.route('/exploits/add')
def add_exploit():
    return render_template("add_exploit.html")
