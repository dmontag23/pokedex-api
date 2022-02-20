import json

import pytest
import respx
from fastapi import HTTPException
from httpx import Response

from app.core.config import settings
from app.tests.fixtures.fun_translations_api_ext \
    import MEWTWO_YODA_JSON_RESPONSE
from app.tests.fixtures.poke_api_ext \
    import POKEMON_SPECIES_MEWTWO_JSON_RESPONSE
from app.utils.external_api_client import send_request


@pytest.mark.parametrize(
    "url,method,return_value",
    [(
            f"{settings.POKE_API_URL}/pokemon-species/mewtwo",
            "GET",
            Response(
                status_code=200,
                json=POKEMON_SPECIES_MEWTWO_JSON_RESPONSE
            )
    ),
        (
                f"{settings.FUN_TRANSLATIONS_API_URL}/yoda",
                "POST",
                Response(
                    status_code=200,
                    json=MEWTWO_YODA_JSON_RESPONSE
                )
        )]
)
@pytest.mark.asyncio
async def test_send_request_success(
        url: str,
        method: str,
        return_value: Response,
        respx_mock
) -> None:
    """Test that the client wrapper is working as expected"""
    # setup mock url
    mocked_api_route = eval(
        f"respx_mock.{method.lower()}(url).mock(return_value)"
    )

    # call the client
    await send_request(url, method)

    request, response = respx.calls.last
    assert mocked_api_route.called
    assert mocked_api_route.call_count == 1
    assert request.url == url
    assert response.status_code == return_value.status_code
    assert response.json() == return_value.json()


@pytest.mark.parametrize(
    "url,method,text,detailed_error_msg",
    [(
            f"{settings.POKE_API_URL}/pokemon-species/mewtwo",
            "GET",
            "Non-json err msg",
            "Non-json err msg"
    ),
        (
                f"{settings.FUN_TRANSLATIONS_API_URL}/yoda",
                "POST",
                json.dumps({"error": {"message": "Json err msg"}}),
                "Json err msg"
        )]
)
@pytest.mark.asyncio
async def test_poke_api_client_fails_on_exception(
        url: str,
        method: str,
        text: str,
        detailed_error_msg: str,
        respx_mock
) -> None:
    """
    Test that the client wrapper raises an exception
    when an error occurs
    """

    # setup mock url
    mocked_poke_api_get_route = eval(
        f"respx_mock.{method.lower()}(url)"
    ).mock(
        Response(
            status_code=404,
            text=text
        )
    )

    # call the client
    with pytest.raises(HTTPException) as err:
        await send_request(url, method)

    request, response = respx.calls.last
    assert mocked_poke_api_get_route.called
    assert mocked_poke_api_get_route.call_count == 1
    assert request.url == url
    assert err.value.status_code == 404
    assert err.value.detail == \
           f"Error when calling {response.url}: {detailed_error_msg}"


@pytest.mark.asyncio
async def test_poke_api_client_fails_on_method_not_implemented(
        respx_mock
) -> None:
    """
    Test that the client wrapper raises an exception
    when using a method not yet implemented
    """

    # setup mock url
    url_to_mock = f"{settings.POKE_API_URL}/pokemon-species/mewtwo"
    mocked_poke_api_get_route = respx_mock.patch(url_to_mock).mock(
        side_effect=HTTPException(status_code=404, detail="Not Found")
    )

    # call the client
    with pytest.raises(HTTPException) as err:
        await send_request(
            f"{settings.POKE_API_URL}/pokemon-species/mewtwo",
            "PATCH"
        )

    assert not mocked_poke_api_get_route.called
    assert err.value.status_code == 405
    assert err.value.detail == \
           "The client does not yet support the PATCH method"
