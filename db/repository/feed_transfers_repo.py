from typing import Sequence, Optional

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import DatabaseEngine
from db.models import FeedTransfers


class FeedTransfersRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def add_feed_transfer(self,
                                volunteer_id: int,
                                user_id: int
                                ) -> bool:
        """

        latitude = Column(Float, nullable=False)
        longitude = Column(Float, nullable=False)

        volunteer_id = Column(BigInteger, ForeignKey('volunteers.id'), nullable=False)
        volunteer: Mapped[CallPoints] = relationship("Volunteers", backref=__tablename__, cascade='all', lazy='subquery')

        user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
        user: Mapped[Users] = relationship("Users", backref=__tablename__, cascade='all', lazy='subquery')
        """
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = FeedTransfers(volunteer_id=volunteer_id, user_id=user_id)
                try:
                    session.add(sql)
                except Exception:
                    return False
                return True

    async def get_feed_transfer_info_by_id(self, feed_transfer_id: int) -> Optional[FeedTransfers]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(FeedTransfers).where(or_(FeedTransfers.id == feed_transfer_id))
                query = await session.execute(sql)
                return query.scalars().one_or_none()

    async def select_all_feed_transfers(self) -> Sequence[FeedTransfers]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(FeedTransfers)
                query = await session.execute(sql)
                return query.scalars().all()

    async def get_feed_transfers_by_volunteer_id(self, volunteer_id: int) -> Sequence[FeedTransfers]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(FeedTransfers).where(or_(FeedTransfers.volunteer_id == volunteer_id))
                query = await session.execute(sql)
                return query.scalars().all()

    async def get_feed_transfers_by_user_id(self, user_id: int) -> Sequence[FeedTransfers]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(FeedTransfers).where(or_(FeedTransfers.user_id == user_id))
                query = await session.execute(sql)
                return query.scalars().all()
