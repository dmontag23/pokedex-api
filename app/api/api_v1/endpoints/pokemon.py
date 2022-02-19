from fastapi import APIRouter, HTTPException
from typing import Any

router = APIRouter()


@router.get("/{pokemon_name}")
def get_pokemon_by_name(
    pokemon_name: str,
) -> Any:
    """
    Fetch a single pokemon by its name
    """
    response = {"message": f"Pokemon name is {pokemon_name}"}

    return response


@router.get("/translated/{pokemon_name}")
def get_pokemon_by_name_translated(
    pokemon_name: str,
) -> Any:
    """
    Fetch a single pokemon by its name and translate its description
    """
    response = {"message": f"Pokemon name is {pokemon_name}"}

    return response