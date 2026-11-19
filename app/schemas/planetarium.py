from apiflask import Schema, fields


class ShowThemeDetailSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class ShowThemeRequestSchema(Schema):
    name = fields.String()
