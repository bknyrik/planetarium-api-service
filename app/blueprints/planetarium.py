from http import HTTPStatus

from flask.views import MethodView
from apiflask import APIBlueprint, HTTPError
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.database.models import planetarium as models
from app.schemas import planetarium as schemas


blueprint = APIBlueprint("planetarium", __name__)


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
