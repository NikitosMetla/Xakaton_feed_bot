from typing import Sequence, Optional

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import DatabaseEngine
from db.models import CallsBaskets


class CallsBasketsRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def add_call_baskets(self,
                               count_feed: int,
                               call_id: int,
                               feed_id: int) -> bool:
        """
        count_feed = Column(Integer, nullable=False, default=0)

        call_id = Column(BigInteger, ForeignKey('calls.id'), nullable=False)
        call: Mapped[CallPoints] = relationship("Calls", backref=__tablename__, cascade='all', lazy='subquery')

        feed_id = Column(BigInteger, ForeignKey('feeds.id'), nullable=False)
        feed: Mapped[Feeds] = relationship("Feeds", backref=__tablename__, cascade='all', lazy='subquery')

        """
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                user = CallsBaskets(call_id=call_id, feed_id=feed_id, count_feed=count_feed)
                try:
                    session.add(user)
                except Exception:
                    return False
                return True

    async def get_call_basket_info_by_id(self, call_basket_id: int) -> Optional[CallsBaskets]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(CallsBaskets).where(or_(CallsBaskets.id == call_basket_id))
                query = await session.execute(sql)
                return query.scalars().one_or_none()

    async def get_call_baskets_by_call_id(self, call_id: int) -> Sequence[CallsBaskets]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(CallsBaskets).where(or_(CallsBaskets.call_id == call_id))
                query = await session.execute(sql)
                return query.scalars().all()

    async def select_all_call_baskets(self) -> Sequence[CallsBaskets]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(CallsBaskets)
                query = await session.execute(sql)
                return query.scalars().all()

    async def get_call_baskets_by_feed_id(self, feed_id: int) -> Sequence[CallsBaskets]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(CallsBaskets).where(or_(CallsBaskets.feed_id == feed_id))
                query = await session.execute(sql)
                return query.scalars().all()