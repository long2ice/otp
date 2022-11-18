from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        alter table otp add column `digest` varchar(32) generated always as (md5(uri)) virtual not null;
create index digest on otp (digest);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        alter table otp drop column digest;
alter table otp drop index digest;"""
