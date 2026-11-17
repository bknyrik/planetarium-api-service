from flask import Flask

from app.utils import application as app_utils


def create_app() -> Flask:
    app = Flask(__name__)

    app_utils.register_extensions(app)

    return app
