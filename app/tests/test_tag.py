import pytest
from httpx import AsyncClient, Response

from app.tests.fixtures import *
from app.tests.functions import get_token


@pytest.mark.anyio
async def test_post(
    async_client: AsyncClient,
    created_post: Response,
    created_tag: Response,
    created_user: Response,
):
    user_token = await get_token(
        username=created_user.json()["email"],
        password="123",
        async_client=async_client,
    )
    post_id = created_post.json()["id"]
    tag_id = created_tag.json()["id"]
    response = await async_client.post(
        f"/api/v1/tag/{tag_id}/post/{post_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 201
    response = await async_client.get(
        f"/api/v1/post",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.status_code == 200
    id_1 = response.json()[0]["id"]
    assert post_id == id_1
    response = await async_client.get(
        f"/api/v1/post/{post_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert response.json()["tags"][0]["id"] == tag_id
