from pydantic import BaseModel


class Pokemon(BaseModel):
    name: str
    description: str
    habitat: str
    isLegendary: str
