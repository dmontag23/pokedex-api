from pydantic import BaseSettings


# The Pydantic BaseSettings class tries to populate the values of these variables from env variables first
class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    class Config:
        case_sensitive = True # match env vars based on case

settings = Settings()
