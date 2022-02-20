from typing import Any

import httpx
from pydantic import Json

from app.core.config import settings


class PokeAPIClient:
    base_url = settings.POKE_API_URL

    @classmethod
    async def send_request(cls, endpoint: str) -> Any:
        async with httpx.AsyncClient(base_url=cls.base_url) as client:
            return await client.get(f"/{endpoint}")


class FunTranslationsAPIClient:
    base_url = settings.FUN_TRANSLATIONS_API_URL

    @classmethod
    async def send_request(cls, endpoint: str, payload: Json) -> Any:
        async with httpx.AsyncClient(base_url=cls.base_url) as client:
            print("POSTING TO", f"{cls.base_url}/{endpoint}")
            return await client.post(f"/{endpoint}", data=payload)
