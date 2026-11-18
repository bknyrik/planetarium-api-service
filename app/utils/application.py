from flask import Flask
from flask_restx import Api

from app import extensions
from app.namespaces import planetarium


def register_extensions(app: Flask) -> None:
    extensions.db.init_app(app)
    extensions.migrate.init_app(app)
    extensions.api.init_app(app)


def register_namespaces(api: Api) -> None:
    api.add_namespace(planetarium.ns)
