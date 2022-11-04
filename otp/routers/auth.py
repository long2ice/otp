import jwt
from fastapi import APIRouter
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from otp.models import User
from otp.settings import JWT_ALGORITHM, settings
from otp.wechat import code_to_session

router = APIRouter()


class LoginBody(BaseModel):
    code: str


UserModel = pydantic_model_creator(User, exclude=("openid",))


class LoginResponse(BaseModel):
    token: str
    user: UserModel  # type: ignore


@router.post("/login", response_model=LoginResponse)
async def login(body: LoginBody):
    session = await code_to_session(body.code)
    user, created = await User.get_or_create(openid=session.openid)
    token = jwt.encode({"user_id": user.pk}, settings.SECRET, algorithm=JWT_ALGORITHM)
    return LoginResponse(token=token, user=UserModel.from_orm(user))
