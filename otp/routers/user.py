from fastapi import APIRouter, Depends

from otp import responses
from otp.depends import auth_required
from otp.models import User

router = APIRouter()


@router.get("", response_model=responses.User)
async def get_user(user: User = Depends(auth_required)):
    return responses.User(expired_date=user.expired_date)
