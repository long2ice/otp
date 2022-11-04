from tortoise import Model, fields


class User(Model):
    nickname = fields.CharField(max_length=50, null=True)
    avatar = fields.CharField(max_length=200, null=True)
    openid = fields.CharField(max_length=200, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Otp(Model):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User")
    secret = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    deleted_at = fields.DatetimeField(null=True)
