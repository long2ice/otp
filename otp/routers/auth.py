import jwt
from fastapi import APIRouter
from pydantic import BaseModel

from otp import responses
from otp.models import User
from otp.settings import JWT_ALGORITHM, settings
from otp.wechat import code_to_session

router = APIRouter()


class LoginBody(BaseModel):
    code: str


@router.post("/login", response_model=responses.LoginResponse)
async def login(body: LoginBody):
    session = await code_to_session(body.code)
    user, created = await User.get_or_create(openid=session.openid)
    token = jwt.encode({"user_id": user.pk}, settings.SECRET, algorithm=JWT_ALGORITHM)
    return responses.LoginResponse(token=token, user=user)
