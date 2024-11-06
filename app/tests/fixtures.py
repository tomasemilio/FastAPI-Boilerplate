import pytest
from httpx import AsyncClient, Response

from app.config import config
from app.tests.functions import get_token


@pytest.fixture
async def admin_token(async_client: AsyncClient) -> str:
    return await get_token(
        username=config.ADMIN_EMAIL,
        password=config.ADMIN_PASSWORD,
        async_client=async_client,
    )


@pytest.fixture
async def created_user(async_client: AsyncClient, admin_token: str) -> Response:
    payload = dict(email="example@example.com", name="example")
    response = await async_client.post(
        "/api/v1/admin/user",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    email = response.json()["email"]
    response = await async_client.get(
        f"/api/v1/user/request-reset-password/{email}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    token = response.json()["message"]
    response = await async_client.post(
        "/api/v1/user/reset-password",
        headers={"Authorization": f"Bearer {token}"},
        json={"password": "123", "confirm_password": "123"},
    )
    return response


@pytest.fixture
async def created_post(async_client: AsyncClient, created_user: Response):
    token = await get_token(
        username=created_user.json()["email"],
        password="123",
        async_client=async_client,
    )
    return await async_client.post(
        "/api/v1/post",
        json=dict(title="test", content="test"),
        headers={"Authorization": f"Bearer {token}"},
    )


@pytest.fixture
async def created_tag(async_client: AsyncClient, created_user: Response):
    token = await get_token(
        username=created_user.json()["email"],
        password="123",
        async_client=async_client,
    )
    return await async_client.post(
        "/api/v1/tag",
        json=dict(name="name", description="description"),
        headers={"Authorization": f"Bearer {token}"},
    )
