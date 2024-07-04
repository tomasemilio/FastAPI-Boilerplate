import pytest
from fastapi import Response
from httpx import AsyncClient, Response

from app.models.user.schemas import UserIn
from app.tests.fixtures import *


@pytest.mark.anyio
async def test_user_crud(
    async_client: AsyncClient, created_user: Response, admin_token: str
):
    response = await async_client.get(
        f"/api/v1/admin/user/{created_user.json()['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    user = response.json()
    password = "new_password"
    new_email = "new" + user["email"]
    new_user = UserIn(
        name=user["name"],
        email=new_email,
        password=password,
    )

    response = await async_client.put(
        f"/api/v1/admin/user/{user['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
        json=new_user.model_dump(),
    )
    updated_user = response.json()
    assert updated_user["email"] == new_email
    response = await async_client.delete(
        f"/api/v1/admin/user/{user['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 204
    response = await async_client.delete(
        f"/api/v1/admin/user/{user['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 404
    response = await async_client.get(
        f"/api/v1/admin/user", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert len(response.json()) == 1
