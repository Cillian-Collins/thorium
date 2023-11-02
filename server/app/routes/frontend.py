from app.db import (
    fetch_exploits,
    fetch_submissions,
    fetch_exploit_name_by_id,
    fetch_services,
    fetch_exploits_breakdown,
    fetch_submissions_breakdown,
    fetch_paginated_submissions,
)
from flask import Blueprint, render_template, abort, request
import os
import sqlite3
import threading


frontend = Blueprint("frontend", __name__)


@frontend.route("/")
def dashboard():
    local = threading.local()

    if not hasattr(local, "conn"):
        local.conn = sqlite3.connect("/database/database.db")

    service_list = fetch_services()

    with open("/stats/time.txt", "r") as f:
        elapsed_time = float(f.read())
        unit_names = ["ms", "s", "m"]
        unit_divisors = [1000, 60, 60]

        for unit_name, unit_divisor in zip(unit_names, unit_divisors):
            if elapsed_time < unit_divisor:
                break
            elapsed_time /= unit_divisor
        elapsed_time = f"{elapsed_time:.2f}{unit_name}"

    return render_template(
        "dashboard.html",
        elapsed_time=elapsed_time,
        service_count=len(service_list),
        exploits=fetch_exploits_breakdown()[0],
        submissions=fetch_submissions_breakdown()[0],
    )


@frontend.route("/submissions")
def submissions():
    local = threading.local()

    if not hasattr(local, "conn"):
        local.conn = sqlite3.connect("/database/database.db")

    page = int(request.args.get("page", 1))

    items = fetch_paginated_submissions(page, 10)
    return render_template("submissions.html", submissions=items, page=page)


@frontend.route("/services")
def services():
    local = threading.local()

    if not hasattr(local, "conn"):
        local.conn = sqlite3.connect("/database/database.db")

    items = fetch_services()
    return render_template("services.html", services=items)


@frontend.route("/services/add")
def add_service():
    return render_template("add_service.html")


@frontend.route("/exploits")
def exploits():
    local = threading.local()

    if not hasattr(local, "conn"):
        local.conn = sqlite3.connect("/database/database.db")

    items = fetch_exploits()
    return render_template("exploits.html", exploits=items)


@frontend.route("/exploits/add")
def add_exploit():
    local = threading.local()

    if not hasattr(local, "conn"):
        local.conn = sqlite3.connect("/database/database.db")

    items = fetch_services()
    return render_template("add_exploit.html", services=items)


@frontend.route("/exploits/<exploit_id>")
def view_exploit(exploit_id):
    local = threading.local()

    if not hasattr(local, "conn"):
        local.conn = sqlite3.connect("/database/database.db")

    exploit_name = fetch_exploit_name_by_id(exploit_id)
    if not exploit_name:
        return abort(404)

    # Define the path to the exploit file
    exploit_file_path = f"/exploits/{exploit_name}"

    # Check if the file exists
    if os.path.isfile(exploit_file_path):
        # If the file exists, read its content
        with open(exploit_file_path, "r") as exploit_file:
            exploit_content = exploit_file.read()
    else:
        # If the file doesn't exist, set the content to an error message or handle it as needed
        exploit_content = "Exploit content not found."

    return render_template(
        "view_exploit.html", exploit_name=exploit_name, exploit_content=exploit_content
    )
