import pytest
from fastapi import Response
from httpx import AsyncClient, Response

from app.tests.fixtures import admin_token, created_post, created_user


@pytest.mark.anyio
async def test_create_user(created_user: Response):
    assert created_user.status_code == 201


@pytest.mark.anyio
async def test_user_integrity(
    async_client: AsyncClient, created_user: Response, admin_token: str
):
    response = await async_client.get(
        "/api/v1/admin/user", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.json()[1]["id"] == created_user.json()["id"]


@pytest.mark.anyio
async def test_create_post_and_cascading_delete(
    async_client: AsyncClient, created_post: Response, admin_token: str
):
    response = await async_client.get(
        "/api/v1/admin/user", headers={"Authorization": f"Bearer {admin_token}"}
    )
    user_id = response.json()[1]["id"]
    assert created_post.json()["user_id"] == user_id
    await async_client.delete(
        f"/api/v1/admin/user/{user_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    response = await async_client.get(
        f"/api/v1/admin/user/{user_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404
