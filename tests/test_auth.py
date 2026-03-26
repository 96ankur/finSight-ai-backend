from __future__ import annotations

from httpx import AsyncClient

REGISTER_URL = "/api/v1/auth/register"
LOGIN_URL = "/api/v1/auth/login"
ME_URL = "/api/v1/auth/me"
REFRESH_URL = "/api/v1/auth/refresh"


async def test_register_user(client: AsyncClient) -> None:
    payload = {
        "email": "test@example.com",
        "password": "strongpassword123",
        "full_name": "Test User",
    }
    response = await client.post(REGISTER_URL, json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["email"] == payload["email"]
    assert data["full_name"] == payload["full_name"]
    assert data["role"] == "user"
    assert data["is_active"] is True
    assert "id" in data


async def test_register_duplicate_email(client: AsyncClient) -> None:
    payload = {
        "email": "dup@example.com",
        "password": "strongpassword123",
        "full_name": "Dup User",
    }
    await client.post(REGISTER_URL, json=payload)
    response = await client.post(REGISTER_URL, json=payload)
    assert response.status_code == 409


async def test_login_and_access_me(client: AsyncClient) -> None:
    payload = {
        "email": "login@example.com",
        "password": "strongpassword123",
        "full_name": "Login User",
    }
    await client.post(REGISTER_URL, json=payload)

    login_response = await client.post(
        LOGIN_URL,
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert login_response.status_code == 200
    tokens = login_response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"

    me_response = await client.get(
        ME_URL,
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == payload["email"]


async def test_login_invalid_credentials(client: AsyncClient) -> None:
    response = await client.post(
        LOGIN_URL,
        json={"email": "no@one.com", "password": "wrong"},
    )
    assert response.status_code == 401


async def test_refresh_token(client: AsyncClient) -> None:
    payload = {
        "email": "refresh@example.com",
        "password": "strongpassword123",
        "full_name": "Refresh User",
    }
    await client.post(REGISTER_URL, json=payload)

    login_resp = await client.post(
        LOGIN_URL,
        json={"email": payload["email"], "password": payload["password"]},
    )
    tokens = login_resp.json()

    refresh_resp = await client.post(
        REFRESH_URL,
        json={"refresh_token": tokens["refresh_token"]},
    )
    assert refresh_resp.status_code == 200
    new_tokens = refresh_resp.json()
    assert "access_token" in new_tokens
    assert "refresh_token" in new_tokens


async def test_me_without_token(client: AsyncClient) -> None:
    response = await client.get(ME_URL)
    assert response.status_code == 401
