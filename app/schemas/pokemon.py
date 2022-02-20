from pydantic import BaseModel


class Pokemon(BaseModel):
    name: str
    description: str
    habitat: str
    isLegendary: str

    class Config:
        schema_extra = {
            "example": {
                "name": "mewtwo",
                "description": "I am mewtwo hear me roar!",
                "habitat": "Someone's mancave",
                "isLegendary": "true"
            }
        }
