from apiflask import APIFlask

from app import extensions
from app.blueprints import planetarium


def register_extensions(app: APIFlask) -> None:
    extensions.db.init_app(app)
    extensions.migrate.init_app(app)

    register_blueprints(app)


def register_blueprints(app: APIFlask) -> None:
    app.register_blueprint(planetarium.blueprint,  url_prefix="/api/planetarium")
