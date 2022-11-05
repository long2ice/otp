from tortoise import Model, fields


class User(Model):
    openid = fields.CharField(max_length=200, unique=True)
    expired_date = fields.DateField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


class Otp(Model):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User")
    uri = fields.CharField(max_length=255, unique=True)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True)

    class Meta:
        unique_together = [("user", "uri")]
