from apiflask import Schema, fields


class ShowThemeSchema(Schema):
    id = fields.Integer()
    name = fields.String()
