from app.db import setup_database
from app.routes.api import api
from app.routes.frontend import frontend
from flask import Flask


def create_app():
    app = Flask(__name__)
    setup_database()

    app.register_blueprint(frontend)
    app.register_blueprint(api, url_prefix="/api")

    return app
