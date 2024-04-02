from app.db import (
    fetch_exploits,
    fetch_submissions,
    fetch_exploit_name_by_id,
    fetch_services,
    fetch_exploits_breakdown,
    fetch_submissions_breakdown,
    fetch_paginated_submissions,
    fetch_targets,
    fetch_disabled_exploits
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
        if elapsed_time < 1:
            elapsed_time *= 1000
            unit_name = "ms"
        elif elapsed_time >= 60:
            elapsed_time /= 60
            unit_name = "m"
        else:
            unit_name = "s"

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


@frontend.route("/targets")
def targets():
    local = threading.local()

    if not hasattr(local, "conn"):
        local.conn = sqlite3.connect("/database/database.db")

    items = fetch_targets()
    return render_template("targets.html", targets=items)


@frontend.route("/targets/add")
def add_targets():
    local = threading.local()

    if not hasattr(local, "conn"):
        local.conn = sqlite3.connect("/database/database.db")

    items = fetch_targets()
    items = "\n".join([item[1] for item in items])
    return render_template("add_targets.html", targets=items)


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

    exploit_file_path = f"/exploits/{exploit_name}"

    if os.path.isfile(exploit_file_path):
        with open(exploit_file_path, "r") as exploit_file:
            exploit_content = exploit_file.read()
    else:
        exploit_content = "Exploit content not found."

    return render_template(
        "view_exploit.html", exploit_name=exploit_name, exploit_content=exploit_content
    )

@frontend.route("/exploits/manage/<exploit_id>")
def manage_exploit(exploit_id):
    local = threading.local()

    if not hasattr(local, "conn"):
        local.conn = sqlite3.connect("/database/database.db")

    exploit_name = fetch_exploit_name_by_id(exploit_id)
    if not exploit_name:
        return abort(404)

    hosts = {}
    for target in fetch_targets():
        hosts[target[1]] = True
    
    print(hosts)

    for exclusion in fetch_disabled_exploits(exploit_id):
        print(exclusion)
        hosts[exclusion[0]] = False
    return render_template("manage_exploit.html", exploit_id=exploit_id, exploit_name=exploit_name, hosts=hosts)
