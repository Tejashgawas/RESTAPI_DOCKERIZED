from marshmallow import Schema, fields, validate

class BookSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1))
    author = fields.String(required=True, validate=validate.Length(min=1))

    