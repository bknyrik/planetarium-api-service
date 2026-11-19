from apiflask import Schema, fields


class ShowThemeDetailResponseSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class ShowThemeRequestSchema(Schema):
    name = fields.String(required=True)


class AstronomyShowDetailResponseSchema(Schema):
    name = fields.String()
    description = fields.String()
    show_themes = fields.Nested(
        ShowThemeDetailResponseSchema(only="name"),
        many=True
    )
