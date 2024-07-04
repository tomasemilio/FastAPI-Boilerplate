from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.functions import get_async_session

sessDep = Annotated[AsyncSession, Depends(get_async_session, use_cache=True)]
