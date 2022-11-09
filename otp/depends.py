import datetime
import hashlib
import json
import time
from json import JSONDecodeError
from typing import Dict

import jwt
from cachetools import TTLCache
from fastapi import Depends, Header, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import constr
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

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


nonce_cache: TTLCache = TTLCache(maxsize=3600, ttl=int(datetime.timedelta(hours=1).total_seconds()))


def get_sign(data: Dict, timestamp: int, nonce: str):
    kvs = [f"timestamp={timestamp}", f"nonce={nonce}"]
    for key, value in data.items():
        if value is None:
            continue
        if isinstance(value, (list, dict)):
            value_str = json.dumps(value)
        else:
            value_str = str(value)
        kvs.append(f"{key}={value_str}")
    to_encode_str = "&".join(sorted(kvs))
    to_encode_str = f"{to_encode_str}&key={settings.API_SECRET}"
    m = hashlib.md5()
    m.update(to_encode_str.encode())
    return m.hexdigest().upper()


async def sign_required(
    request: Request,
    x_sign: str = Header(..., example="sign"),
    x_nonce: constr(curtail_length=8) = Header(..., example="11111111"),  # type:ignore
    x_timestamp: int = Header(..., example=int(time.time())),
):
    if request.url.path in ["/docs", "/openapi.json"]:
        return
    if request.method in ["GET", "DELETE"]:
        data = dict(request.query_params)
    else:
        try:
            data = await request.json()
        except JSONDecodeError:
            data = {}
    now = int(datetime.datetime.now().timestamp())
    if abs(now - x_timestamp) > 60 * 10:
        raise HTTPException(detail="Timestamp expired", status_code=HTTP_403_FORBIDDEN)
    if x_nonce in nonce_cache:
        raise HTTPException(detail="Nonce str repeated", status_code=HTTP_403_FORBIDDEN)
    nonce_cache[x_nonce] = True
    verified = get_sign(data, x_timestamp, x_nonce) == x_sign
    if not verified:
        raise HTTPException(detail="Signature verify failed", status_code=HTTP_403_FORBIDDEN)
