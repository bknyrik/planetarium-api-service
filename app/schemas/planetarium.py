from marshmallow import Schema, fields


class ShowThemeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()
