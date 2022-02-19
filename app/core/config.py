from pydantic import BaseSettings


# The Pydantic BaseSettings class tries to populate the values
# of these variables from env variables first
class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    POKE_API_URL: str = "https://pokeapi.co/api/v2"
    TRANSLATOR_API_URL: str = "https://api.funtranslations.com/translate"

    class Config:
        case_sensitive = True  # match env vars based on case


settings = Settings()
