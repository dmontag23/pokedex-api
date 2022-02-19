import pytest
from fastapi.testclient import TestClient

from app.main import app


# set up the client to send requests to our api
@pytest.fixture(scope="module")
def base_app_client():
    client = TestClient(app)
    # client.base_url += settings.API_V1_STR  -- this would be set if using api versioning
    yield client