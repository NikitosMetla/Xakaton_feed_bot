from typing import Sequence, Optional

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import DatabaseEngine
from db.models import VolunteersBaskets


class VolunteersBasketsRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def add_volunteers_basket(self,
                                    volunteer_id: int,
                                    feed_id: int,
                                    count_feed: int,
                                    ) -> bool:
        """

        count_feed = Column(Integer, nullable=False, default=0)

        feed_id = Column(BigInteger, ForeignKey('feeds.id'), nullable=True)
        feed: Mapped[Feeds] = relationship("Feeds", backref=__tablename__, cascade='all', lazy='subquery')

        volunteer_id = Column(BigInteger, ForeignKey('volunteers.id'), nullable=False)
        volunteer: Mapped[Volunteers] = relationship("Volunteers", backref=__tablename__, cascade='all', lazy='subquery')

        """
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = VolunteersBaskets(count_feed=count_feed, feed_id=feed_id, volunteer_id=volunteer_id)
                try:
                    session.add(sql)
                except Exception:
                    return False
                return True

    async def get_volunteer_basket_info_by_id(self, volunteer_basket_id: int) -> Optional[VolunteersBaskets]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(VolunteersBaskets).where(or_(VolunteersBaskets.id == volunteer_basket_id))
                query = await session.execute(sql)
                return query.scalars().one_or_none()

    async def select_all_volunteer_baskets(self) -> Sequence[VolunteersBaskets]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(VolunteersBaskets)
                query = await session.execute(sql)
                return query.scalars().all()

    async def get_volunteer_baskets_by_feed_id(self, feed_id: int) -> Sequence[VolunteersBaskets]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(VolunteersBaskets).where(or_(VolunteersBaskets.feed_id == feed_id))
                query = await session.execute(sql)
                return query.scalars().all()

    async def get_volunteer_baskets_by_volunteer_id(self, volunteer_id: int) -> Sequence[VolunteersBaskets]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(VolunteersBaskets).where(or_(VolunteersBaskets.volunteer_id == volunteer_id))
                query = await session.execute(sql)
                return query.scalars().all()
