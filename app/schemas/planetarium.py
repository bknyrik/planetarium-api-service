from apiflask import Schema, fields


class ShowThemeDetailResponseSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class ShowThemeRequestSchema(Schema):
    name = fields.String(required=True)
