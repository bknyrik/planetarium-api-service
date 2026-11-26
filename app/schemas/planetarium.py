from apiflask import Schema, fields, validators
from marshmallow import post_load, ValidationError

from app.extensions import db
from app.database.models import planetarium as models


class ShowThemeDetailResponseSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class ShowThemeRequestSchema(Schema):
    name = fields.String(required=True)


class ShowThemePartialUpdateRequestSchema(Schema):
    name = fields.String(dump_default=None)


class AstronomyShowDetailResponseSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    description = fields.String()
    show_themes = fields.Pluck(
        ShowThemeDetailResponseSchema,
        field_name="name",
        many=True
    )


class AstronomyShowExtendDetailResponseSchema(
    AstronomyShowDetailResponseSchema
):
    show_themes = fields.Nested(ShowThemeDetailResponseSchema, many=True)


class AstronomyShowRequestSchema(Schema):
    name = fields.String()
    description = fields.String(allow_none=True)
    show_themes = fields.List(fields.Integer, required=False)

    @post_load
    def load_show_themes_by_ids(self, input_data: dict, **kwargs) -> dict:
        input_ids = input_data["show_themes"]
        input_data["show_themes"] = db.session.scalars(
            db.select(models.ShowThemeModel)
            .where(models.ShowThemeModel.id.in_(input_ids))
        ).all()

        show_theme_ids = tuple(
            map(lambda st: st.id, input_data["show_themes"])
        )
        for id_ in input_ids:
            if id_ not in show_theme_ids:
                raise ValidationError(
                    message=f"Show theme by '{id_}' does not exist."
                )

        return input_data


class PlanetariumDomeDetailResponseSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    rows = fields.Integer()
    seats_in_row = fields.Integer()


class PlanetariumDomeRequestSchema(Schema):
    name = fields.String()
    rows = fields.Integer()
    seats_in_row = fields.Integer()
