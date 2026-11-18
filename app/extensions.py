from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restx import Api


db = SQLAlchemy()
migrate = Migrate(db=db, directory="app/database/migrations")
api = Api(prefix="/api")
