from http import HTTPStatus

from flask.views import MethodView
from apiflask import APIBlueprint, HTTPError, EmptySchema
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.database.models import planetarium as models
from app.schemas import planetarium as schemas


blueprint = APIBlueprint("planetarium", __name__)


@blueprint.route("/show_themes/")
class ShowThemeListAPIView(MethodView):

    @blueprint.output(list[schemas.ShowThemeDetailResponseSchema])
    def get(self) -> list[models.ShowThemeModel]:
        return db.session.scalars(db.select(models.ShowThemeModel)).all()

    @blueprint.input(schemas.ShowThemeRequestSchema)
    @blueprint.output(schemas.ShowThemeDetailResponseSchema, status_code=201)
    def post(self, json_data: dict) -> models.ShowThemeModel:
        try:
            instance = models.ShowThemeModel(**json_data)

            db.session.add(instance)
            db.session.commit()
            db.session.refresh(instance)

            return instance
        except SQLAlchemyError:
            db.session.rollback()
            raise HTTPError(
                detail="An error occurred while show theme creation",
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR
            )


@blueprint.route("/show_themes/<int:pk>/")
class ShowThemeDetailAPIView(MethodView):

    @blueprint.output(schemas.ShowThemeDetailResponseSchema)
    def get(self, pk: int) -> models.ShowThemeModel:
        return db.get_or_404(models.ShowThemeModel, ident=pk)

    @blueprint.output(schemas.ShowThemeDetailResponseSchema)
    @blueprint.input(schemas.ShowThemeRequestSchema)
    def put(self, pk: int, json_data: dict) -> models.ShowThemeModel:
        try:
            instance = db.get_or_404(models.ShowThemeModel, ident=pk)
            instance.name = json_data["name"]

            db.session.commit()

            return instance
        except SQLAlchemyError:
            db.session.rollback()
            raise HTTPError(
                detail="An error occurred while updating the show theme",
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR
            )

    @blueprint.output(schemas.ShowThemeDetailResponseSchema)
    @blueprint.input(schemas.ShowThemeRequestSchema)
    def patch(self, pk: int, json_data: dict) -> models.ShowThemeModel:
        try:
            instance = db.get_or_404(models.ShowThemeModel, ident=pk)
            instance.name = json_data.get("name", instance.name)

            db.session.commit()
            return instance
        except SQLAlchemyError:
            db.session.rollback()
            raise HTTPError(
                detail="An error occurred while updating the the show theme",
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR
            )

    @blueprint.output(EmptySchema, status_code=HTTPStatus.NO_CONTENT)
    def delete(self, pk: int) -> None:
        try:
            instance = db.get_or_404(models.ShowThemeModel, ident=pk)
            db.session.delete(instance)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise HTTPError(
                detail="An error occurred while show theme deletion",
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR
            )


@blueprint.route("/astronomy_shows/")
class AstronomyShowListAPIView(MethodView):

    @blueprint.output(list[schemas.AstronomyShowDetailResponseSchema])
    def get(self) -> list[models.AstronomyShowModel]:
        return db.session.scalars(db.select(models.AstronomyShowModel)).all()

    @blueprint.output(schemas.AstronomyShowDetailResponseSchema)
    @blueprint.input(schemas.AstronomyShowRequestSchema)
    def post(self, json_data: dict) -> models.AstronomyShowModel:
        try:
            show_themes_ids = json_data.pop("show_themes", ())
            instance = models.AstronomyShowModel(**json_data)

            instance.show_themes = (
                db
                .session
                .scalars(
                    db.select(models.ShowThemeModel)
                    .where(models.ShowThemeModel.id.in_(show_themes_ids))
                ).all()
            )

            db.session.add(instance)
            db.session.commit()
            db.session.refresh(instance)
            return instance
        except SQLAlchemyError:
            db.session.rollback()
            raise HTTPError(
                detail="An error occurred while astronomy show creation",
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR
            )


@blueprint.route("/astronomy_shows/<int:pk>")
class AstronomyShowDetailAPIView(MethodView):

    @blueprint.output(schemas.AstronomyShowExtendDetailResponseSchema)
    def get(self, pk: int) -> models.AstronomyShowModel:
        return db.get_or_404(models.AstronomyShowModel, ident=pk)

    @blueprint.output(schemas.AstronomyShowDetailResponseSchema)
    @blueprint.input(schemas.AstronomyShowRequestSchema)
    def put(self, pk: int, json_data: dict) -> models.AstronomyShowModel:
        try:
            instance = db.get_or_404(models.AstronomyShowModel, ident=pk)

            for name, value in json_data.items():
                setattr(instance, name, value)

            db.session.commit()
            return instance
        except SQLAlchemyError:
            db.session.rollback()
            raise HTTPError(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating astronomy show"
            )

    @blueprint.output(EmptySchema, status_code=HTTPStatus.NO_CONTENT)
    def delete(self, pk: int) -> None:
        try:
            instance = db.get_or_404(models.AstronomyShowModel, ident=pk)
            db.session.delete(instance)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise HTTPError(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail="An error occurred while astronomy show deletion"
            )
