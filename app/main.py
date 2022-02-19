from fastapi import FastAPI

from app.api.api_v1.api import api_router

app = FastAPI(title="Pokedex API")

# setup routers for the api

# for a production env, I would normally version the api by setting a prefix (shown below),
# but this does not conform with the original design specs where no version is specified
# app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(api_router)
