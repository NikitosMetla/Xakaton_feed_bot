from typing import Sequence, Optional

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import DatabaseEngine
from db.models import ReceivingAlbums


class ReceivingAlbumsRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def add_call_album(self,
                                    photo_id: str,
                                    call_id: int,
                                    ) -> bool:
        """

        photo_id = Column(String, nullable=False)

        call_id = Column(BigInteger, ForeignKey('calls.id'), nullable=False)
        call: Mapped[Calls] = relationship("Calls", backref=__tablename__, cascade='all', lazy='subquery')

        """
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = ReceivingAlbums(photo_id=photo_id, call_id=call_id)
                try:
                    session.add(sql)
                except Exception:
                    return False
                return True

    async def get_receiving_album_info_by_id(self, receiving_album_id: int) -> Optional[ReceivingAlbums]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(ReceivingAlbums).where(or_(ReceivingAlbums.id == receiving_album_id))
                query = await session.execute(sql)
                return query.scalars().one_or_none()

    async def select_all_receiving_albums(self) -> Sequence[ReceivingAlbums]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(ReceivingAlbums)
                query = await session.execute(sql)
                return query.scalars().all()

    async def get_receiving_albums_by_call_id(self, call_id: int) -> Sequence[ReceivingAlbums]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(ReceivingAlbums).where(or_(ReceivingAlbums.call_id == call_id))
                query = await session.execute(sql)
                return query.scalars().all()

