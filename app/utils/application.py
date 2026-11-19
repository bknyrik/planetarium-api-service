from apiflask import APIFlask

from app import extensions


def register_extensions(app: APIFlask) -> None:
    extensions.db.init_app(app)
    extensions.migrate.init_app(app)
