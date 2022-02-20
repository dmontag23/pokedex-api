from typing import List

from app.schemas.poke_api_ext import PokemonExtResponse
from app.schemas.pokemon import Pokemon


def map_pokemon_ext_response_to_pokemon(pokemon_species: PokemonExtResponse) \
        -> Pokemon:
    en_descriptions: List[str] = \
        [flavor_text.flavor_text
         for flavor_text in pokemon_species.flavor_text_entries
         if flavor_text.language.name == "en"]

    return Pokemon(
        name=pokemon_species.name,
        description=en_descriptions[0].replace('\n', ' ').replace('\f', ' '),
        habitat=pokemon_species.habitat.name,
        isLegendary=str(pokemon_species.is_legendary).lower()
    )
