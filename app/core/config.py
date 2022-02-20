from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Class used to set up urls available across the app
    This class sets default values for environment variables
    if that environment variable is not found
    """
    API_V1_STR: str = "/api/v1"
    POKE_API_URL: str = "https://pokeapi.co/api/v2"
    FUN_TRANSLATIONS_API_URL: str = "https://api.funtranslations.com/translate"

    class Config:
        case_sensitive = True  # match env vars based on case


settings = Settings()
