import pytest
from httpx import Response

from app.api.api_v1.endpoints.pokemon \
    import get_pokemon_object, translate_pokemon_description
from app.core.config import settings
from app.schemas.pokemon import Pokemon
from app.tests.fixtures.fun_translations_api_ext \
    import MEWTWO_YODA_JSON_RESPONSE, \
    PIKACHU_SHAKESPEARE_JSON_RESPONSE, \
    ZUBAT_YODA_JSON_RESPONSE
from app.tests.fixtures.poke_api_ext \
    import POKEMON_SPECIES_MEWTWO_JSON_RESPONSE, \
    POKEMON_SPECIES_PIKACHU_JSON_RESPONSE, \
    POKEMON_SPECIES_ZUBAT_JSON_RESPONSE

ROUTE_PREFIX = "/pokemon"
MEWTWO_DATA_TRANSLATED = {
    "name": "mewtwo",
    "description": "Created by a scientist after years of "
                   "horrific gene splicing and dna engineering experiments, "
                   "it was.",
    "habitat": "rare",
    "isLegendary": "true"
}
PIKACHU_DATA_TRANSLATED = {
    "name": "pikachu",
    "description": "At which hour several of these pokémon gather, "
                   "their electricity couldst buildeth "
                   "and cause lightning storms.",
    "habitat": "forest",
    "isLegendary": "false"
}

ZUBAT_DATA_TRANSLATED = {
    "name": "zubat",
    "description": "Forms colonies in perpetually dark places. "
                   "Ultrasonic waves to identify and "
                   "approach targets, it uses.",
    "habitat": "cave",
    "isLegendary": "false"
}


@pytest.mark.asyncio
async def test_get_pokemon_object(respx_mock) -> None:
    """Test getting a correct pokemon object"""

    # setup mock url
    pokemon_name = "mewtwo"
    mocked_poke_api_get_route = respx_mock.get(
        f"{settings.POKE_API_URL}/pokemon-species/{pokemon_name}"
    ).mock(
        return_value=Response(
            status_code=200,
            json=POKEMON_SPECIES_MEWTWO_JSON_RESPONSE
        ))

    pokemon = await get_pokemon_object(pokemon_name)

    assert mocked_poke_api_get_route.called
    assert mocked_poke_api_get_route.call_count == 1
    assert pokemon.name == "mewtwo"
    assert pokemon.description == \
           "It was created by a scientist after years of " \
           "horrific gene splicing and DNA engineering experiments."
    assert pokemon.habitat == "rare"
    assert pokemon.isLegendary == 'true'


@pytest.mark.parametrize(
    "input_pokemon,\
    mock_fun_translation_url_suffix,\
    mock_fun_translation_response,\
    expected_pokemon",
    [
        (
                Pokemon(
                    name="mewtwo",
                    description="It was created by a scientist after years "
                                "of horrific gene splicing and DNA "
                                "engineering experiments.",
                    habitat="rare",
                    isLegendary="true"),
                "yoda", MEWTWO_YODA_JSON_RESPONSE,
                Pokemon(
                    name="mewtwo",
                    description="Created by a scientist after years of "
                                "horrific gene splicing and "
                                "dna engineering experiments, it was.",
                    habitat="rare",
                    isLegendary="true")
        ),
        (
                Pokemon(
                    name="pikachu",
                    description="When several of these POKéMON gather, "
                                "their electricity could build and cause "
                                "lightning storms.",
                    habitat="forest",
                    isLegendary="false"),
                "shakespeare", PIKACHU_SHAKESPEARE_JSON_RESPONSE,
                Pokemon(
                    name="pikachu",
                    description="At which hour several of these pokémon "
                                "gather, their electricity couldst buildeth "
                                "and cause lightning storms.",
                    habitat="forest",
                    isLegendary="false")
        ),
        (
                Pokemon(
                    name="zubat",
                    description="Forms colonies in perpetually dark places. "
                                "Uses ultrasonic waves to identify and "
                                "approach targets.",
                    habitat="cave",
                    isLegendary="false"),
                "yoda", ZUBAT_YODA_JSON_RESPONSE,
                Pokemon(
                    name="zubat",
                    description="Forms colonies in perpetually dark places. "
                                "Ultrasonic waves to identify and "
                                "approach targets, it uses.",
                    habitat="cave",
                    isLegendary="false"
                )
        )
    ]
)
@pytest.mark.asyncio
async def test_translate_pokemon_description(
        input_pokemon: Pokemon,
        mock_fun_translation_url_suffix: str,
        mock_fun_translation_response: dict[str, str],
        expected_pokemon: Pokemon,
        respx_mock
) -> None:
    """Test translating a pokemon's description"""

    # setup mock url
    mocked_fun_translations_api_post_route = respx_mock.post(
        f"{settings.FUN_TRANSLATIONS_API_URL}/"
        f"{mock_fun_translation_url_suffix}") \
        .mock(
        return_value=Response(
            status_code=200,
            json=mock_fun_translation_response
        ))

    pokemon = await translate_pokemon_description(input_pokemon)

    assert mocked_fun_translations_api_post_route.called
    assert mocked_fun_translations_api_post_route.call_count == 1
    assert pokemon.name == expected_pokemon.name
    assert pokemon.description == expected_pokemon.description
    assert pokemon.habitat == expected_pokemon.habitat
    assert pokemon.isLegendary == expected_pokemon.isLegendary


@pytest.mark.asyncio
async def test_get_pokemon_by_name_success(
        async_app_client,
        respx_mock
) -> None:
    """Test the pokemon/<pokemon name> endpoint is working as expected"""

    pokemon_name = "mewtwo"
    expected_returned_data = {
        "name": pokemon_name,
        "description": "It was created by a scientist after years of horrific"
                       " gene splicing and DNA engineering experiments.",
        "habitat": "rare",
        "isLegendary": "true"
    }

    # setup mock url
    mocked_poke_api_get_route = respx_mock.get(
        f"{settings.POKE_API_URL}/pokemon-species/{pokemon_name}"
    ).mock(
        return_value=Response(
            status_code=200,
            json=POKEMON_SPECIES_MEWTWO_JSON_RESPONSE
        )
    )

    response: Response = await async_app_client.get(
        f"{ROUTE_PREFIX}/{pokemon_name}"
    )

    assert mocked_poke_api_get_route.called
    assert mocked_poke_api_get_route.call_count == 1
    assert response.status_code == 200
    assert response.json() == expected_returned_data


@pytest.mark.parametrize(
    "pokemon_name,\
    mock_poke_api_response,\
    mock_fun_translation_url_suffix,\
    mock_fun_translation_response,\
    expected_return_data",
    [(
            "mewtwo",
            POKEMON_SPECIES_MEWTWO_JSON_RESPONSE,
            "yoda",
            MEWTWO_YODA_JSON_RESPONSE,
            MEWTWO_DATA_TRANSLATED
    ),
        (
                "pikachu",
                POKEMON_SPECIES_PIKACHU_JSON_RESPONSE,
                "shakespeare",
                PIKACHU_SHAKESPEARE_JSON_RESPONSE,
                PIKACHU_DATA_TRANSLATED
        ),
        (
                "zubat",
                POKEMON_SPECIES_ZUBAT_JSON_RESPONSE,
                "yoda",
                ZUBAT_YODA_JSON_RESPONSE,
                ZUBAT_DATA_TRANSLATED
        )]
)
@pytest.mark.asyncio
async def test_get_pokemon_by_name_translated_success(
        pokemon_name: str,
        mock_poke_api_response: dict[str, str],
        mock_fun_translation_url_suffix: str,
        mock_fun_translation_response: dict[str, str],
        expected_return_data: dict[str, str],
        async_app_client,
        respx_mock
) -> None:
    """
    Test the pokemon/translated/<pokemon name> endpoint
    is working as expected
    """

    # setup mock urls
    mocked_poke_api_get_route = respx_mock.get(
        f"{settings.POKE_API_URL}/pokemon-species/{pokemon_name}") \
        .mock(return_value=Response(status_code=200,
                                    json=mock_poke_api_response))
    mocked_fun_translations_api_post_route = respx_mock.post(
        f"{settings.FUN_TRANSLATIONS_API_URL}"
        f"/{mock_fun_translation_url_suffix}") \
        .mock(return_value=Response(status_code=200,
                                    json=mock_fun_translation_response))

    response: Response = await async_app_client.get(
        f"{ROUTE_PREFIX}/translated/{pokemon_name}"
    )

    assert mocked_poke_api_get_route.called
    assert mocked_poke_api_get_route.call_count == 1
    assert mocked_fun_translations_api_post_route.called
    assert mocked_fun_translations_api_post_route.call_count == 1
    assert response.status_code == 200
    assert response.json() == expected_return_data
