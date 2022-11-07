from fastapi import APIRouter, Depends

from otp.depends import auth_required, sign_required
from otp.routers import auth, feedback, icon, otp, user

router = APIRouter()
signed_router = APIRouter(dependencies=[Depends(sign_required)])
no_signed_router = APIRouter()

signed_router.include_router(
    user.router, prefix="/user", tags=["User"], dependencies=[Depends(auth_required)]
)
signed_router.include_router(
    otp.router, prefix="/otp", tags=["OTP"], dependencies=[Depends(auth_required)]
)
signed_router.include_router(
    feedback.router, prefix="/feedback", tags=["Feedback"], dependencies=[Depends(auth_required)]
)
signed_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
no_signed_router.include_router(icon.router, prefix="/icon", tags=["Icon"])

router.include_router(signed_router)
router.include_router(no_signed_router)
