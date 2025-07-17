from marshmallow import fields,Schema,validate

class RegisterSchema(Schema):
        username = fields.Str(required=True, validate=validate.Length(min=3))
        email    = fields.Email(required=True)
        password = fields.Str(required=True, validate=validate.Length(min=6))

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)