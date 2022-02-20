import pytest
from httpx import Response


@pytest.mark.asyncio
async def test_health(async_app_client, respx_mock) -> None:
    """Test the health endpoint returns an ok status"""

    response: Response = await async_app_client.get("/health")
    assert response.status_code == 200
    assert response.json().get("status") == "ok"
