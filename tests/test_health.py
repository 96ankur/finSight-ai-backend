from __future__ import annotations

from httpx import AsyncClient


async def test_health_endpoint(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "environment" in data
