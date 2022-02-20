from typing import List

from pydantic import BaseModel


class Habitat(BaseModel):
    name: str


class Language(BaseModel):
    name: str


class FlavorText(BaseModel):
    flavor_text: str
    language: Language


class PokemonExtResponse(BaseModel):
    name: str
    flavor_text_entries: List[FlavorText]
    habitat: Habitat
    is_legendary: bool
