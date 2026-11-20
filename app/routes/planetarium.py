from http import HTTPStatus

from flask.views import MethodView
from apiflask import APIBlueprint, HTTPError, EmptySchema
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.database.models import planetarium as models
from app.schemas import planetarium as schemas
from app.routes import shortcuts


blueprint = APIBlueprint("planetarium", __name__)


@blueprint.route("/show_themes/")
class ShowThemeListAPIView(shortcuts.ListCreateAPIView):
    model_name = "Show theme"
    model_type = models.ShowThemeModel

    @blueprint.output(list[schemas.ShowThemeDetailResponseSchema])
    def get(self, *args, **kwargs) -> list[models.ShowThemeModel]:
        return super().get(*args, **kwargs)

    @blueprint.input(schemas.ShowThemeRequestSchema)
    @blueprint.output(
        schema=schemas.ShowThemeDetailResponseSchema,
        status_code=HTTPStatus.CREATED
    )
    def post(self, *args, **kwargs) -> models.ShowThemeModel:
        return super().post(*args, **kwargs)


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
class AstronomyShowListAPIView(
    shortcuts.ListCreateAPIView[models.AstronomyShowModel]
):
    model_type = models.AstronomyShowModel
    model_name = "astronomy show"

    @blueprint.output(list[schemas.AstronomyShowDetailResponseSchema])
    def get(self, *args, **kwargs) -> list[models.AstronomyShowModel]:
        return super().get(*args, **kwargs)

    @blueprint.output(schemas.AstronomyShowDetailResponseSchema)
    @blueprint.input(schemas.AstronomyShowRequestSchema)
    def post(self, *args, **kwargs) -> models.AstronomyShowModel:
        return super().post(*args, **kwargs)


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
