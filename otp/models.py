from tortoise import Model, fields


class TimestampedModel(Model):
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class User(TimestampedModel):
    openid = fields.CharField(max_length=200, unique=True)
    is_cloud_enabled = fields.BooleanField(default=False)
    expired_date = fields.DateField(null=True)


class DigestField(fields.CharField):  # type: ignore
    has_db_field = False


class Otp(TimestampedModel):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User")
    uri = fields.CharField(max_length=255, unique=True)
    digest = DigestField(max_length=32, unique=True)
    is_active = fields.BooleanField(default=True)
    deleted_at = fields.DatetimeField(null=True)

    class Meta:
        unique_together = [("user", "uri")]


class Feedback(TimestampedModel):
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User")
    content = fields.TextField()
