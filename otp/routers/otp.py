from fastapi import APIRouter, Depends
from pydantic import BaseModel

from otp.depends import auth_required
from otp.models import Otp

router = APIRouter()


class OTPBody(BaseModel):
    secret: str


@router.post("")
async def create_otp(body: OTPBody, user=Depends(auth_required)):
    await Otp.create(user=user, secret=body.secret)


@router.get("")
async def get_otp():
    pass
