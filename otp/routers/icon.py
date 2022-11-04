from io import BytesIO

from fastapi import APIRouter
from starlette.responses import FileResponse, StreamingResponse

from otp.settings import DEFAULT_ICON_PATH
from otp.tfa import get_issuer_domain, get_tfa_icon

router = APIRouter()


@router.get("/{issuer}.svg")
async def get_issuer_icon(issuer: str):
    domain = get_issuer_domain(issuer)
    response = FileResponse(DEFAULT_ICON_PATH, media_type="image/svg+xml")
    cache_control = "public, max-age=86400"
    response.headers["Cache-Control"] = cache_control
    if not domain:
        return response
    else:
        icon = await get_tfa_icon(domain)
        if not icon:
            return response
        response = StreamingResponse(BytesIO(icon), media_type="image/svg+xml")
        response.headers["Cache-Control"] = cache_control
        return response
