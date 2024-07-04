import pytest
from httpx import AsyncClient, Response

from app.tests.fixtures import *
from app.tests.functions import get_token


@pytest.mark.anyio
async def test_post(
    async_client: AsyncClient,
    created_post: Response,
    created_user: Response,
    admin_token: str,
):
    user_token = await get_token(
        username=created_user.json()["email"],
        password="123",
        async_client=async_client,
    )
    post_id = created_post.json()["id"]
    response = await async_client.get(
        f"/api/v1/post/{post_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200
    response = await async_client.delete(
        f"/api/v1/admin/user/{created_user.json()['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 204
    response = await async_client.get(
        f"/api/v1/post/{post_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 404
    response = await async_client.get(
        f"/api/v1/user/{post_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404
