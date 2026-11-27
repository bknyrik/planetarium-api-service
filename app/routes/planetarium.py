from http import HTTPStatus

from apiflask import APIBlueprint, EmptySchema

from app.extensions import db
from app.database.models import planetarium as models
from app.schemas import planetarium as schemas
from app.routes import shortcuts


blueprint = APIBlueprint("planetarium", __name__)


@blueprint.route("/show_themes/")
class ShowThemeListAPIView(
    shortcuts.ListCreateAPIView[models.ShowThemeModel]
):
    model_name = "Show theme"
    model_type = models.ShowThemeModel

    @blueprint.output(list[schemas.ShowThemeDetailResponseSchema])
    @blueprint.doc(
        summary="Get show theme list"
    )
    def get(self, *args, **kwargs) -> list[models.ShowThemeModel]:
        return super().get(*args, **kwargs)

    @blueprint.input(schemas.ShowThemeRequestSchema)
    @blueprint.output(
        schema=schemas.ShowThemeDetailResponseSchema,
        status_code=HTTPStatus.CREATED
    )
    @blueprint.doc(
        summary="Create show theme"
    )
    def post(self, *args, **kwargs) -> models.ShowThemeModel:
        return super().post(*args, **kwargs)


@blueprint.route("/show_themes/<int:pk>/")
class ShowThemeDetailAPIView(
    shortcuts.RetrieveUpdateDestroyAPIView[models.ShowThemeModel]
):
    model_type = models.ShowThemeModel
    model_name = "Show theme"

    @blueprint.output(schemas.ShowThemeDetailResponseSchema)
    @blueprint.doc(
        summary="Get show theme detail"
    )
    def get(self, *args, **kwargs) -> models.ShowThemeModel:
        return super().get(*args, **kwargs)

    @blueprint.output(schemas.ShowThemeDetailResponseSchema)
    @blueprint.input(schemas.ShowThemeRequestSchema)
    @blueprint.doc(
        summary="Completely update show theme"
    )
    def put(self, *args, **kwargs) -> models.ShowThemeModel:
        return super().put(*args, **kwargs)

    @blueprint.output(schemas.ShowThemeDetailResponseSchema)
    @blueprint.input(schemas.ShowThemePartialUpdateRequestSchema)
    @blueprint.doc(
        summary="Partially update show theme"
    )
    def patch(self, *args, **kwargs) -> models.ShowThemeModel:
        return super().patch(*args, **kwargs)

    @blueprint.output(EmptySchema, status_code=HTTPStatus.NO_CONTENT)
    @blueprint.doc(
        summary="Delete show theme"
    )
    def delete(self, *args, **kwargs) -> None:
        return super().delete(*args, **kwargs)


@blueprint.route("/astronomy_shows/")
class AstronomyShowListAPIView(
    shortcuts.ListCreateAPIView[models.AstronomyShowModel]
):
    model_type = models.AstronomyShowModel
    model_name = "astronomy show"

    def get_object_list(
        self,
        *args,
        **kwargs
    ) -> list[models.AstronomyShowModel]:
        result = db.session.scalars(
            db.select(self.model_type)
            .options(db.joinedload(self.model_type.show_themes))
        )
        return result.unique().all()

    @blueprint.output(list[schemas.AstronomyShowDetailResponseSchema])
    @blueprint.doc(
        summary="Get astronomy show list"
    )
    def get(self, *args, **kwargs) -> list[models.AstronomyShowModel]:
        return super().get(*args, **kwargs)

    @blueprint.output(
        schemas.AstronomyShowDetailResponseSchema,
        status_code=HTTPStatus.CREATED
    )
    @blueprint.input(schemas.AstronomyShowRequestSchema)
    def post(self, *args, **kwargs) -> models.AstronomyShowModel:
        return super().post(*args, **kwargs)


@blueprint.route("/astronomy_shows/<int:pk>")
class AstronomyShowDetailAPIView(
    shortcuts.RetrieveUpdateDestroyAPIView[models.AstronomyShowModel]
):
    model_type = models.AstronomyShowModel
    model_name = "Astronomy show"

    @blueprint.output(schemas.AstronomyShowExtendDetailResponseSchema)
    def get(self, *args, **kwargs) -> models.AstronomyShowModel:
        return super().get(*args, **kwargs)

    @blueprint.output(schemas.AstronomyShowDetailResponseSchema)
    @blueprint.input(schemas.AstronomyShowRequestSchema)
    def put(self, *args, **kwargs) -> models.AstronomyShowModel:
        return super().put(*args, **kwargs)

    @blueprint.output(EmptySchema, status_code=HTTPStatus.NO_CONTENT)
    def delete(self, *args, **kwargs) -> None:
        return super().patch(*args, **kwargs)


@blueprint.route("/planetarium_domes/")
class PlanetariumDomeListAPIView(
    shortcuts.ListCreateAPIView[models.PlanetariumDomeModel]
):
    model_type = models.PlanetariumDomeModel
    model_name = "Planetarium Dome"

    @blueprint.output(list[schemas.PlanetariumDomeDetailResponseSchema])
    def get(self, *args, **kwargs) -> list[models.PlanetariumDomeModel]:
        return super().get(*args, **kwargs)

    @blueprint.output(
        schema=schemas.PlanetariumDomeDetailResponseSchema,
        status_code=HTTPStatus.CREATED
    )
    @blueprint.input(schemas.PlanetariumDomeRequestSchema)
    def post(self, *args, **kwargs) -> models.PlanetariumDomeModel:
        return super().post(*args, **kwargs)
