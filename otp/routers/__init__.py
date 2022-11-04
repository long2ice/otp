from fastapi import APIRouter, Depends

from otp.depends import auth_required
from otp.routers import auth, icon, otp, user

router = APIRouter()

router.include_router(
    user.router, prefix="/user", tags=["User"], dependencies=[Depends(auth_required)]
)
router.include_router(
    otp.router, prefix="/otp", tags=["OTP"], dependencies=[Depends(auth_required)]
)
router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(icon.router, prefix="/icon", tags=["Icon"])
