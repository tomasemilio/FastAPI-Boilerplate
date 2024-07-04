import pytest
from httpx import Response

from app.tests.fixtures import *


@pytest.mark.anyio
async def test_registration(created_user: Response):
    assert created_user.status_code == 200
    verified = created_user.json()["verified"]
    assert verified
