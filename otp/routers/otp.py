import hashlib
from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from tortoise import timezone

from otp.depends import auth_required, cloud_enabled
from otp.models import Otp
from otp.responses import Recycle

router = APIRouter()


class OTPBody(BaseModel):
    uris: List[str]


class DeleteBody(BaseModel):
    uri: str


@router.post("", dependencies=[Depends(cloud_enabled)])
async def add_otp_list(body: OTPBody, user=Depends(auth_required)):
    for uri in body.uris:
        await Otp.get_or_create(user=user, uri=uri)


@router.get("", response_model=List[str])
async def get_otp_list(user=Depends(auth_required)):
    data = (
        await Otp.filter(user=user, is_active=True, deleted_at=None)
        .order_by("-id")
        .values_list("uri", flat=True)
    )
    return data


@router.get("/recycle", response_model=List[Recycle])
async def get_otp_recycle_list(user=Depends(auth_required)):
    data = (
        await Otp.filter(user=user, is_active=False, deleted_at=None)
        .order_by("-id")
        .values("id", "uri", "updated_at")
    )
    return data


@router.put("", dependencies=[Depends(cloud_enabled)])
async def delete_otp(body: DeleteBody, user=Depends(auth_required)):
    digest = hashlib.md5(body.uri.encode()).hexdigest()
    await Otp.filter(digest=digest, user=user).update(is_active=False)


@router.delete("/{pk}/recycle", dependencies=[Depends(cloud_enabled)])
async def delete_recycle(pk: int, user=Depends(auth_required)):
    await Otp.filter(pk=pk, user=user).update(deleted_at=timezone.now())


@router.put("/{pk}/restore", dependencies=[Depends(cloud_enabled)])
async def restore_otp(pk: int, user=Depends(auth_required)):
    await Otp.filter(pk=pk, user=user).update(is_active=True)
