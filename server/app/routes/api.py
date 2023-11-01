from flask import Blueprint, render_template

api = Blueprint("api", __name__)


@api.route('/exploits/add')
def add_exploit():
    return render_template("add_exploit.html")

