from http import HTTPStatus

from apiflask import HTTPError
from flask_sqlalchemy.model import Model
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db


class ListModelMixin:
    model_type: type[Model]
    model_name: str

    def list(self, *args, **kwargs) -> list[Model]:
        try:
            return db.session.scalars(db.select(self.model_type)).all()
        except SQLAlchemyError:
            raise HTTPError(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while {self.model_name} creation"
            )
