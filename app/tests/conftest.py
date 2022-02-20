from typing import Generator

import pytest_asyncio
from httpx import AsyncClient

from app.main import app


@pytest_asyncio.fixture
async def async_app_client() -> Generator[AsyncClient, None, None]:
    """Create an async client to make requests to the api"""
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client
