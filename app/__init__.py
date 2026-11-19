from apiflask import APIFlask

from app.utils import application as app_utils


def create_app(config: str = "app.settings.DevelopmentConfig") -> APIFlask:
    app = APIFlask(__name__)
    app.config.from_object(config)

    app_utils.register_extensions(app)

    return app
