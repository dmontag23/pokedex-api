from fastapi import APIRouter

from app.api.api_v1.endpoints import pokemon

# Set up all sub-routers with the appropriate prefix
api_v1_router = APIRouter()
api_v1_router.include_router(
    pokemon.router, prefix="/pokemon", tags=["pokemon"]
)
