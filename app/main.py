from logging.config import dictConfig

from fastapi import FastAPI

from app.api.api_v1.api import api_router
from app.schemas.health import Health
from app.schemas.log_config import LogConfig

dictConfig(LogConfig().dict())  # setup logging config

app = FastAPI(title="Pokedex API")

# setup routers for the api

# for a production env, I would normally version the api by setting a prefix,
# but this does not conform with the original design specs
# app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(api_router)


# the health endpoint is here because it will never be versioned
@app.get("/health", tags=["health"], response_model=Health)
def health():
    return {"status": "ok"}
