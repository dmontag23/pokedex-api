import pytest
import respx
from fastapi import HTTPException
from httpx import Response

from app.core.config import settings
from app.tests.fixtures.fun_translations_api_ext \
    import MEWTWO_YODA_JSON_REQUEST, MEWTWO_YODA_JSON_RESPONSE
from app.tests.fixtures.poke_api_ext \
    import POKEMON_SPECIES_MEWTWO_JSON_RESPONSE
from app.utils.external_api_clients \
    import FunTranslationsAPIClient, PokeAPIClient


@pytest.mark.asyncio
async def test_poke_api_client_success(respx_mock) -> None:
    """Test that the PokeAPIClient is working as expected"""
    # setup mock url
    url_to_mock = f"{settings.POKE_API_URL}/pokemon-species/mewtwo"
    mocked_poke_api_get_route = respx_mock.get(url_to_mock).mock(
        return_value=Response(
            status_code=200,
            json=POKEMON_SPECIES_MEWTWO_JSON_RESPONSE)
    )

    # call the client
    await PokeAPIClient.send_request("pokemon-species/mewtwo")

    request, response = respx.calls.last
    assert mocked_poke_api_get_route.called
    assert mocked_poke_api_get_route.call_count == 1
    assert request.url == url_to_mock
    assert response.status_code == 200
    assert response.json() == POKEMON_SPECIES_MEWTWO_JSON_RESPONSE


@pytest.mark.asyncio
async def test_poke_api_client_fails(respx_mock) -> None:
    """Test that the PokeAPIClient raises an exception when an error occurs"""

    # setup mock url
    url_to_mock = f"{settings.POKE_API_URL}/pokemon-species/mewtwo"
    mocked_poke_api_get_route = respx_mock.get(url_to_mock).mock(
        side_effect=HTTPException(status_code=404, detail="Not Found")
    )

    # call the client
    with pytest.raises(HTTPException) as err:
        await PokeAPIClient.send_request("pokemon-species/mewtwo")

    request, response = respx.calls.last
    assert mocked_poke_api_get_route.called
    assert mocked_poke_api_get_route.call_count == 1
    assert request.url == url_to_mock
    assert response is None
    assert err.value.status_code == 404
    assert err.value.detail == "Not Found"


@pytest.mark.asyncio
async def test_fun_translations_api_client_success(respx_mock) -> None:
    """Test that the FunTranslationsAPIClient is working as expected"""

    # setup mock url
    url_to_mock = f"{settings.FUN_TRANSLATIONS_API_URL}/yoda"
    mocked_fun_translations_api_post_route = respx_mock.post(url_to_mock).mock(
        return_value=Response(status_code=200, json=MEWTWO_YODA_JSON_RESPONSE))

    # call the client
    await FunTranslationsAPIClient.send_request(
        "yoda",
        payload=MEWTWO_YODA_JSON_REQUEST
    )

    request, response = respx.calls.last
    assert mocked_fun_translations_api_post_route.called
    assert mocked_fun_translations_api_post_route.call_count == 1
    assert request.url == url_to_mock
    assert MEWTWO_YODA_JSON_REQUEST.get('text') \
           in request.content.decode('utf-8').replace("+", " ")
    assert response.status_code == 200
    assert response.json() == MEWTWO_YODA_JSON_RESPONSE


@pytest.mark.asyncio
async def test_fun_translations_api_client_fails(respx_mock) -> None:
    """
    Test that the FunTranslationsAPIClient raises
    an exception when an error occurs
    """

    # setup mock url
    url_to_mock = f"{settings.FUN_TRANSLATIONS_API_URL}/yoda"
    mocked_poke_api_get_route = respx_mock.post(url_to_mock).mock(
        side_effect=HTTPException(status_code=404, detail="Not Found")
    )

    # call the client
    with pytest.raises(HTTPException) as err:
        await FunTranslationsAPIClient.send_request(
            "yoda",
            payload=MEWTWO_YODA_JSON_REQUEST
        )

    request, response = respx.calls.last
    assert mocked_poke_api_get_route.called
    assert mocked_poke_api_get_route.call_count == 1
    assert request.url == url_to_mock
    assert response is None
    assert err.value.status_code == 404
    assert err.value.detail == "Not Found"
