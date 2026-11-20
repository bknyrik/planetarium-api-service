from http import HTTPStatus

from apiflask import HTTPError
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db


class ListModelMixin[T]:
    model_type: type[T]
    model_name: str

    def list(self, *args, **kwargs) -> list[T]:
        try:
            return db.session.scalars(db.select(self.model_type)).all()
        except SQLAlchemyError:
            raise HTTPError(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while getting '{self.model_name}' list"
            )


class CreateModelMixin[T]:
    model_type: type[T]
    model_name: str

    def create(self, *args, **kwargs) -> T:
        try:
            json_data: dict = kwargs["json_data"]

            multiple_data = {}

            for key, value in json_data.copy().items():
                multiple_data[key] = json_data.pop(key)

            instance = self.model_type(**json_data)

            for key, value in multiple_data.items():
                setattr(instance, key, value)

            db.session.add(instance)
            db.session.commit()
            db.session.refresh(
                instance=instance,
                attribute_names=tuple(multiple_data.keys()),
            )

            return instance
        except SQLAlchemyError:
            db.session.rollback()
            raise HTTPError(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while {self.model_name} creation"
            )
