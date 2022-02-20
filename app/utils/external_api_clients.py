from typing import Any

import httpx
from pydantic import Json

from app.core.config import settings
from app.core.logger import logger


class PokeAPIClient:
    base_url = settings.POKE_API_URL

    @classmethod
    async def send_request(cls, endpoint: str) -> Any:
        async with httpx.AsyncClient(base_url=cls.base_url) as client:
            logger.info("Attempting to get pokemon data from "
                        f"{cls.base_url}/{endpoint}")
            return await client.get(f"/{endpoint}")


class FunTranslationsAPIClient:
    base_url = settings.FUN_TRANSLATIONS_API_URL

    @classmethod
    async def send_request(cls, endpoint: str, payload: Json) -> Any:
        async with httpx.AsyncClient(base_url=cls.base_url) as client:
            logger.info("Attempting to get translation data from "
                        f"{cls.base_url}/{endpoint}")
            logger.debug(f"The payload provided is {payload}")
            return await client.post(f"/{endpoint}", data=payload)
