import os

from dotenv import load_dotenv


load_dotenv()


class BaseConfig:
    APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SECRET_KEY = os.getenv("SECRET_KEY")


class DevelopmentConfig(BaseConfig):
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv("POSTGRES_USER")}"
        f":{os.getenv("POSTGRES_PASSWORD")}"
        f"@{os.getenv("POSTGRES_HOST")}"
        f":{os.getenv("POSTGRES_PORT")}"
        f"/{os.getenv("POSTGRES_DB")}"
    )
    SQLALCHEMY_ENGINE_OPTIONS = {
        "echo": True
    }
