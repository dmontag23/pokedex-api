import json

from fastapi import HTTPException, status
from httpx import AsyncClient, Response

from app.core.logger import logger


async def send_request(
        url: str,
        method: str,
        payload:
        dict[str, str] = {}
) -> Response:
    async with AsyncClient() as client:
        logger.info(f"Attempting to {method} data:  "
                    f"{url}")
        logger.debug(f"The payload provided is {payload}")

        match method:
            case "GET":
                response: Response = await client.get(
                    f"{url}",
                )
            case "POST":
                response: Response = await client.post(
                    f"{url}",
                    data=payload
                )
            case _:
                raise HTTPException(
                    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                    detail=f"The client does not yet support the"
                           f" {method} method"
                )

        if not response.is_success:
            logger.error(f"Error calling {response.url}: "
                         f"Response is {response.text}")
            try:
                error_message = json.loads(response.text)
                error_message = error_message.get('error').get('message')
            except ValueError:
                logger.info("Could not convert error "
                            "from external api to json")
                error_message = response.text
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error when calling {response.url}: "
                       f"{error_message}"
            )

        return response
