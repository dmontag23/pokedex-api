import json

from fastapi import HTTPException, status
from httpx import AsyncClient, Response

from app.core.logger import logger


async def send_request(
        url: str,  # noqa
        method: str,
        payload: dict[str, str] = {}
) -> Response:
    """
    Implements a custom client wrapper to make
    external HTTP requests

    There are a lot of improvements that could be made:
    - Handling errors from external apis could make use
      of respective api error schemas
    - The response from the external api could be cached
    """

    async with AsyncClient() as client:  # noqa
        logger.debug("The payload provided to the wrapper client "
                     f"when calling {url} is {payload}")

        # check currently implemented methods
        implemented_methods = ["GET", "POST"]
        if method not in implemented_methods:
            logger.error(f"Method {method} is not currently implemented")
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail=f"The client does not yet support the "
                       f"{method} method"
            )

        # build client call
        suffix = ")" if method == "GET" else ", data=payload)"
        response: Response = await eval(
            f"client.{method.lower()}(url{suffix}"
        )

        # handle errors - this section could be refactored
        # to better handle any errors that come back from the
        # client by utilizing the client error schema(s)
        if not response.is_success:
            logger.error(f"Error calling {response.url}: "
                         f"Response is {response.text}")

            # the following try/except attempts to get the error message
            # from the client.
            # it assumes the error is returned in the form:
            # {"error": {"message": "this is the error message"}}
            # which is what fun translations api errors return
            try:
                error_message = json.loads(response.text)
                logger.info("Json converted error message "
                            f"is {error_message}")
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
