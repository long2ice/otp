from tortoise import Model, fields


class User(Model):
    email = fields.CharField(max_length=255, unique=True)
    secret = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Otp(Model):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User")
    secret = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    deleted_at = fields.DatetimeField(null=True)
