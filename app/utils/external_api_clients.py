import json

from fastapi import HTTPException
from httpx import AsyncClient, Response
from pydantic import Json

from app.core.config import settings
from app.core.logger import logger


class PokeAPIClient:
    base_url = settings.POKE_API_URL

    @classmethod
    async def send_request(cls, endpoint: str) -> Response:
        async with AsyncClient(base_url=cls.base_url) as client:
            logger.info("Attempting to get pokemon data from "
                        f"{cls.base_url}/{endpoint}")

            response: Response = await client.get(f"/{endpoint}")

            if not response.is_success:
                logger.error(f"Error calling {response.url}: "
                             f"Response is {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Error when calling {response.url}: "
                           f"{response.text}"
                )

            return response


class FunTranslationsAPIClient:
    base_url = settings.FUN_TRANSLATIONS_API_URL

    @classmethod
    async def send_request(cls, endpoint: str, payload: Json) -> Response:
        async with AsyncClient(base_url=cls.base_url) as client:
            logger.info("Attempting to get translation data from "
                        f"{cls.base_url}/{endpoint}")
            logger.debug(f"The payload provided is {payload}")

            response: Response = await client.post(f"/{endpoint}", data=payload)

            if not response.is_success:
                logger.error(f"Error calling {response.url}: "
                             f"Response is {response.text}")
                try:
                    error_message = json.loads(response.text)
                    error_message = error_message.get('error').get('message')
                except ValueError:
                    logger.info("Could not convert error from external api to json")
                    error_message = response.text
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Error when calling {response.url}: "
                           f"{error_message}"
                )

            return response
