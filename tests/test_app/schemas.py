from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.Str()
    password = fields.Str()


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class BotSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str()


bot_schema = BotSchema()
bots_schema = BotSchema(many=True)
