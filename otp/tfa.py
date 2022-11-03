import os

import aiofiles
import httpx

from otp.settings import TFA_ICON_DIR

_data = {}


async def init():
    global _data
    url = 'https://2fa.directory/api/v3/tfa.json'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
    for item in data:
        _data[item[0].lower()] = item[1]


def get_issuer_domain(issuer: str):
    data = _data.get(issuer.lower())
    if data:
        return data.get('domain')
    return None


async def get_tfa_icon(domain: str):
    icon_name = f'{domain}.svg'
    icon_path = os.path.join(TFA_ICON_DIR, icon_name)
    if os.path.exists(icon_path):
        async with aiofiles.open(icon_path, 'rb') as f:
            return await f.read()
    else:
        url = f'https://raw.githubusercontent.com/2factorauth/twofactorauth/master/img/{domain[0]}/{icon_name}'
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            async with aiofiles.open(icon_path, mode='wb') as f:
                await f.write(response.content)
                return response.content
