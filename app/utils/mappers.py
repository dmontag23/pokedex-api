from app.core.logger import logger
from app.schemas.poke_api_ext import PokemonExtResponse
from app.schemas.pokemon import Pokemon


def map_pokemon_ext_response_to_pokemon(
        pokemon_from_ext_response: PokemonExtResponse
) -> Pokemon:
    """Maps schemas PokemonExtResponse -> Pokemon"""

    logger.debug("Called map_pokemon_ext_response_to_pokemon with pokemon "
                 f"{pokemon_from_ext_response.json()}")

    # filter out all non-english descriptions
    en_descriptions = \
        [flavor_text.flavor_text
         for flavor_text in pokemon_from_ext_response.flavor_text_entries
         if flavor_text.language.name == "en"]

    return Pokemon(
        name=pokemon_from_ext_response.name,
        description=en_descriptions[0].replace('\n', ' ').replace('\f', ' '),
        habitat=pokemon_from_ext_response.habitat.name,
        isLegendary=str(pokemon_from_ext_response.is_legendary).lower()
    )
