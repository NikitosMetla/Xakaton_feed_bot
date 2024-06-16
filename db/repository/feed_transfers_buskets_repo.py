from typing import Sequence, Optional

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import DatabaseEngine
from db.models import FeedTransfersBuskets


class FeedTransfersBasketsRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def add_feed_transfers_basket(self,
                                        count_feed: int,
                                        feed_id: int,
                                        feed_transfer_id: int,
                                        ) -> bool:
        """

         count_feed = Column(Integer, nullable=False, default=0)

        feed_id = Column(BigInteger, ForeignKey('feeds.id'), nullable=True)
        feed: Mapped[Feeds] = relationship("Feeds", backref=__tablename__, cascade='all', lazy='subquery')

        feed_transfer_id = Column(BigInteger, ForeignKey('feed_transfers.id'), nullable=False)
        feed_transfer: Mapped[FeedTransfers] = relationship("FeedTransfers", backref=__tablename__, cascade='all',
                                                        lazy='subquery')
        """
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = FeedTransfersBuskets(count_feed=count_feed, feed_id=feed_id, feed_transfer_id=feed_transfer_id)
                try:
                    session.add(sql)
                except Exception:
                    return False
                return True

    async def get_feed_transfer_basket_info_by_id(self, feed_transfer_basket_id: int) -> Optional[FeedTransfersBuskets]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(FeedTransfersBuskets).where(or_(FeedTransfersBuskets.id == feed_transfer_basket_id))
                query = await session.execute(sql)
                return query.scalars().one_or_none()

    async def select_all_feed_transfer_baskets(self) -> Sequence[FeedTransfersBuskets]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(FeedTransfersBuskets)
                query = await session.execute(sql)
                return query.scalars().all()

    async def get_feed_transfer_baskets_by_feed_transfer_id(self, feed_transfer_id: int) -> Sequence[FeedTransfersBuskets]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(FeedTransfersBuskets).where(or_(FeedTransfersBuskets.feed_transfer_id == feed_transfer_id))
                query = await session.execute(sql)
                return query.scalars().all()

    async def get_feed_transfer_baskets_by_feed_id(self, feed_id: int) -> Sequence[FeedTransfersBuskets]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(FeedTransfersBuskets).where(or_(FeedTransfersBuskets.feed_id == feed_id))
                query = await session.execute(sql)
                return query.scalars().all()
