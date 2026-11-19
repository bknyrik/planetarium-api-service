from http import HTTPStatus

from flask.views import MethodView
from apiflask import APIBlueprint, HTTPError, EmptySchema
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.database.models import planetarium as models
from app.schemas import planetarium as schemas


blueprint = APIBlueprint("planetarium", __name__, url_prefix="/planetarium")


@blueprint.route("/show_themes/")
class ShowThemeListAPIView(MethodView):

    @blueprint.output(list[schemas.ShowThemeDetailSchema])
    def get(self) -> list[models.ShowThemeModel]:
        return db.session.scalars(db.select(models.ShowThemeModel)).all()

    @blueprint.input(schemas.ShowThemeRequestSchema)
    @blueprint.output(schemas.ShowThemeDetailSchema, status_code=201)
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

    @blueprint.output(schemas.ShowThemeDetailSchema)
    def get(self, pk: int) -> models.ShowThemeModel:
        return db.get_or_404(models.ShowThemeModel, ident=pk)

    @blueprint.output(schemas.ShowThemeDetailSchema)
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
