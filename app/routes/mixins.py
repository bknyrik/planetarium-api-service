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
            instance = self.model_type(**json_data)

            db.session.add(instance)
            db.session.commit()
            db.session.refresh(instance)

            return instance
        except SQLAlchemyError:
            db.session.rollback()
            raise HTTPError(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while {self.model_name} creation"
            )


class DetailMixin[T]:
    model_type: type[T]
    model_name: str

    def get_object(self, pk: int) -> T:
        instance = db.session.scalars(
            db.select(self.model_type)
            .where(self.model_type.id == pk)
        ).first()

        if not instance:
            raise HTTPError(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"{self.model_name.title()} with id {pk} not found"
            )

        return instance


class RetrieveModelMixin[T]:
    model_type: type[T]
    model_name: str

    def retrieve(self, *args, **kwargs) -> T:
        try:
            instance = self.get_object(kwargs["pk"])
            return instance
        except SQLAlchemyError:
            raise HTTPError(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while getting '{self.model_name}'"
            )


class DestroyModelMixin[T]:
    model_type: type[T]
    model_name: str

    def destroy(self, *args, **kwargs) -> None:
        try:
            instance = self.get_object(kwargs["pk"])
            db.session.delete(instance)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise HTTPError(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while {self.model_name} deletion"
            )


class ListCreateModelMixin[T](
    ListModelMixin[T],
    CreateModelMixin[T]
):
    ...
