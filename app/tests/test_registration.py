import pytest
from httpx import AsyncClient, Response

from app.tests.fixtures import admin_token, registered_user


@pytest.mark.anyio
async def test_registration(async_client: AsyncClient, registered_user: Response):
    assert registered_user.status_code == 201
    verified = registered_user.json()["verified"]
    email = registered_user.json()["email"]
    id = registered_user.json()["id"]
    assert not verified
    response = await async_client.get(f"/api/v1/user/request_verification/{email}")
    verification_token = response.json()["token"]
    response = await async_client.get(f"/api/v1/user/verify?token={verification_token}")
    assert response.status_code == 200
    verified_user = response.json()
    assert verified_user["verified"]
    assert verified_user["id"] == id
