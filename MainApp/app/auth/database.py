from typing import AsyncGenerator, Optional

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.models import UP
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User

from model.database import sessionLocal


class MySQLAlchemyUserDatabase(SQLAlchemyUserDatabase):

    async def get_by_username(self, login: str) -> Optional[UP]:
        statement = select(self.user_table).where(
            self.user_table.login == login
        )
        return await self._get_user(statement)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessionLocal() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield MySQLAlchemyUserDatabase(session, User)
