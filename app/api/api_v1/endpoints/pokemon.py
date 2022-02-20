from typing import Any

from fastapi import APIRouter

from app.core.config import settings
from app.core.logger import logger
from app.schemas.fun_translations_api_ext \
    import TranslationsExtCreate, TranslationsExtResponse
from app.schemas.poke_api_ext import PokemonExtResponse
from app.schemas.pokemon import Pokemon
from app.utils.external_api_clients import send_request
from app.utils.mappers import map_pokemon_ext_response_to_pokemon

router = APIRouter()


async def get_pokemon_object(name: str) -> Pokemon:
    """Gets a pokemon by its name"""
    logger.debug(f"Called get_pokemon_object with name {name}")
    response = await send_request(
        f"{settings.POKE_API_URL}/pokemon-species/{name}",
        "GET"
    )
    logger.debug("Response status code from poke api client is "
                 f"{response.status_code}")
    logger.debug("Response json from poke api client is "
                 f"{response.json()}")
    pokemon_data = map_pokemon_ext_response_to_pokemon(
        PokemonExtResponse(**response.json())
    )
    return pokemon_data


async def translate_pokemon_description(
        original_pokemon: Pokemon
) -> Pokemon:
    """Returns the pokemon provided but with a translated description"""

    logger.debug("Called translate_pokemon_description with pokemon"
                 f" {original_pokemon.json()}")

    # construct the request to the translations api
    path = "yoda" \
        if original_pokemon.habitat == "cave" \
           or original_pokemon.isLegendary == "true" \
        else "shakespeare"
    translation_payload = TranslationsExtCreate(
        text=original_pokemon.description
    ).json()

    # get the response from the translations api
    # and translate it into a schema object
    response = await send_request(
        f"{settings.FUN_TRANSLATIONS_API_URL}/{path}",
        "POST",
        translation_payload
    )
    logger.debug("Response status code from fun "
                 f"translations client is {response.status_code}")
    logger.debug("Response json from fun "
                 f"translations client is {response.json()}")
    translation_data = TranslationsExtResponse(**response.json())

    # return a new pokemon with the modified description
    pokemon_to_return = original_pokemon.copy()
    pokemon_to_return.description = translation_data.contents.translated
    return pokemon_to_return


@router.get("/{pokemon_name}", response_model=Pokemon)
async def get_pokemon_by_name(
        pokemon_name: str,
) -> Any:
    """
    Fetch a single pokemon by its name
    """
    logger.info(f"Called /{pokemon_name} endpoint")
    pokemon = await get_pokemon_object(pokemon_name)
    return pokemon


@router.get("/translated/{pokemon_name}", response_model=Pokemon)
async def get_pokemon_by_name_translated(
        pokemon_name: str,
) -> Any:
    """
    Fetch a single pokemon by its name and translate its description
    """
    logger.info(f"Called translated/{pokemon_name} endpoint")
    pokemon = await get_pokemon_object(pokemon_name)
    pokemon_with_translated_description = \
        await translate_pokemon_description(pokemon)
    return pokemon_with_translated_description
