from typing import Sequence, Optional

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import DatabaseEngine
from db.models import TransfersAlbums


class TransfersAlbumsRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def add_transfer_album(self,
                                    photo_id: str,
                                    feed_transfer_id: int,
                                    ) -> bool:
        """

        photo_id = Column(String, nullable=False)

        feed_transfer_id = Column(BigInteger, ForeignKey('feed_transfers.id'), nullable=False)
        feed_transfer: Mapped[FeedTransfers] = relationship("FeedTransfers", backref=__tablename__, cascade='all', lazy='subquery')

        """
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = TransfersAlbums(photo_id=photo_id, feed_transfer_id=feed_transfer_id)
                try:
                    session.add(sql)
                except Exception:
                    return False
                return True

    async def get_transfer_album_info_by_id(self, transfer_album_id: int) -> Optional[TransfersAlbums]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(TransfersAlbums).where(or_(TransfersAlbums.id == transfer_album_id))
                query = await session.execute(sql)
                return query.scalars().one_or_none()

    async def select_all_transfer_albums(self) -> Sequence[TransfersAlbums]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(TransfersAlbums)
                query = await session.execute(sql)
                return query.scalars().all()

    async def get_transfer_albums_by_feed_transfer_id(self, feed_transfer_id: int) -> Sequence[TransfersAlbums]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(TransfersAlbums).where(or_(TransfersAlbums.feed_transfer_id == feed_transfer_id))
                query = await session.execute(sql)
                return query.scalars().all()

