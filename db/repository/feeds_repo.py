from typing import Sequence, Optional

from sqlalchemy import select, update, or_
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import DatabaseEngine
from db.models import Feeds


class FeedsRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def add_feed(self, kind_of_animal: str, category: str):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                point = Feeds(kind_of_animal=kind_of_animal,
                              category_of_feed=category)
                try:
                    session.add(point)
                except Exception:
                    return False
                return True

    async def select_all_feeds(self) -> Sequence[Feeds]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Feeds)
                query = await session.execute(sql)
                return query.scalars().all()

    async def select_feed_by_id(self, feed_id: int) -> Optional[Feeds]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Feeds).where(or_(Feeds.id == feed_id))
                query = await session.execute(sql)
                return query.scalars().one_or_none()
