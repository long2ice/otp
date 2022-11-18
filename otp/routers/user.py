from fastapi import APIRouter, Depends
from pydantic import BaseModel

from otp import responses
from otp.depends import auth_required
from otp.models import User

router = APIRouter()


@router.get("", response_model=responses.User)
async def get_user(user: User = Depends(auth_required)):
    return user


class UpdateUserBody(BaseModel):
    is_cloud_enabled: bool


@router.put("", response_model=responses.User)
async def update_user(body: UpdateUserBody, user: User = Depends(auth_required)):
    user.is_cloud_enabled = body.is_cloud_enabled
    await user.save(update_fields=["is_cloud_enabled"])
    return user
