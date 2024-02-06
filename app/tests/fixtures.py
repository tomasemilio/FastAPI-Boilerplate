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
    payload = dict(
        name="test",
        password="test",
        confirm_password="test",
        email="test@test.com",
        scope=["user"],
    )
    response = await async_client.post(
        "/api/v1/admin/user",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    return response


@pytest.fixture
async def created_post(async_client: AsyncClient, created_user: Response):
    token = await get_token(
        username=created_user.json()["email"],
        password="test",
        async_client=async_client,
    )
    return await async_client.post(
        "/api/v1/post",
        json=dict(title="test", content="test"),
        headers={"Authorization": f"Bearer {token}"},
    )
