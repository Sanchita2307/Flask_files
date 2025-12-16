from marshmallow import Schema, fields, post_load
from models.user_models import User

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    mobile = fields.Int(required=True)
    salary = fields.Float(required=True)
    password = fields.Str(load_only=True, required=True) 
    is_deleted = fields.Bool(required=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)