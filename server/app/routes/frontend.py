from app.db import fetch_exploits, fetch_submissions, fetch_exploit_name_by_id
from flask import Blueprint, render_template, abort
import os
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


@frontend.route('/exploits/<exploit_id>')
def view_exploit(exploit_id):
    local = threading.local()

    if not hasattr(local, "conn"):
        local.conn = sqlite3.connect('/database/database.db')

    exploit_name = fetch_exploit_name_by_id(exploit_id)
    if not exploit_name:
        return abort(404)

    # Define the path to the exploit file
    exploit_file_path = f'/exploits/{exploit_name}'

    # Check if the file exists
    if os.path.isfile(exploit_file_path):
        # If the file exists, read its content
        with open(exploit_file_path, 'r') as exploit_file:
            exploit_content = exploit_file.read()
    else:
        # If the file doesn't exist, set the content to an error message or handle it as needed
        exploit_content = "Exploit content not found."

    return render_template("view_exploit.html", exploit_name=exploit_name, exploit_content=exploit_content)
