import jwt
from fastapi import HTTPException, Header
from starlette.status import HTTP_401_UNAUTHORIZED

from otp.models import User
from otp.settings import settings


async def auth_required(authorization: str = Header(...)):
    invalid_token = HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")
    try:
        data = jwt.decode(authorization, settings.SECRET, algorithms=["HS256"])
    except jwt.DecodeError:
        raise invalid_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token expired")
    user_id = data.get("user_id")
    if not user_id:
        raise invalid_token
    user = await User.get_or_none(pk=user_id)
    if not user:
        raise invalid_token
    return user
