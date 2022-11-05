import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_401_UNAUTHORIZED

from otp.models import User
from otp.settings import JWT_ALGORITHM, settings

auth_scheme = HTTPBearer()


async def auth_required(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    invalid_token = HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")
    try:
        data = jwt.decode(token.credentials, settings.SECRET, algorithms=[JWT_ALGORITHM])
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
