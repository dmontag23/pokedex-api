from app.schemas.poke_api_ext import PokemonExtResponse
from app.tests.fixtures.poke_api_ext \
    import POKEMON_SPECIES_PIKACHU_JSON_RESPONSE
from app.utils.mappers import map_pokemon_ext_response_to_pokemon


def test_map_pokemon_ext_response_to_pokemon() -> None:
    """Test mapping PokemonExtResponse -> Pokemon"""
    pikachu_pokemon_species_display = \
        PokemonExtResponse(**POKEMON_SPECIES_PIKACHU_JSON_RESPONSE)
    pikachu_pokemon_display = \
        map_pokemon_ext_response_to_pokemon(pikachu_pokemon_species_display)

    assert pikachu_pokemon_display.name == "pikachu"
    assert pikachu_pokemon_display.description == \
           "When several of these POKéMON gather, " \
           "their electricity could build and cause lightning storms."
    assert pikachu_pokemon_display.habitat == "forest"
    assert pikachu_pokemon_display.isLegendary == 'false'
