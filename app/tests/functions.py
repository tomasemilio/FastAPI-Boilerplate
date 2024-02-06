from httpx import AsyncClient


async def get_token(username: str, password: str, async_client: AsyncClient) -> str:
    response = await async_client.post(
        "/api/v1/auth/token",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return response.json()["access_token"]
