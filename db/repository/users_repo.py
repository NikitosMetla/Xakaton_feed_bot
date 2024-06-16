from typing import Sequence

from sqlalchemy import select, update, or_
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import DatabaseEngine
from db.models import Users


class UserRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def add_user(self, user_id: int, username: str):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                user = Users(user_id=user_id, username=username)
                try:
                    session.add(user)
                except Exception:
                    return False
                return True

    async def get_user_by_user_id(self, user_id: int) -> Users:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Users).where(or_(Users.user_id == user_id))
                query = await session.execute(sql)
                return query.scalars().one_or_none()

    async def select_all_users(self) -> Sequence[Users]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Users)
                query = await session.execute(sql)
                return query.scalars().all()

