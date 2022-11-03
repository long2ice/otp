from io import BytesIO

import httpx
from fastapi import APIRouter
from starlette.responses import FileResponse, StreamingResponse

from otp.settings import DEFAULT_ICON_PATH
from otp.tfa import get_issuer_domain, get_tfa_icon

router = APIRouter()


@router.get("/{issuer}.svg")
async def get_issuer_icon(issuer: str):
    domain = get_issuer_domain(issuer)
    default_response = FileResponse(DEFAULT_ICON_PATH, media_type="image/svg+xml")
    if not domain:
        return default_response
    else:
        icon = await get_tfa_icon(domain)
        if not icon:
            return default_response
        return StreamingResponse(BytesIO(icon), media_type="image/svg+xml")
