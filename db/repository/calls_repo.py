from typing import Sequence, Optional

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import DatabaseEngine
from db.models import Calls


class CallsRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def add_call(self,
                       call_point_id: int,
                       volunteer_id: int,
                       ) -> bool:
        """

        call_point_id = Column(BigInteger, ForeignKey('call_points.id'), nullable=False)
        call_point: Mapped[CallPoints] = relationship("CallPoints", backref=__tablename__, cascade='all', lazy='subquery')

        volunteer_id = Column(BigInteger, ForeignKey('volunteers.id'), nullable=False)
        volunteer: Mapped[Volunteers] = relationship("Volunteers", backref=__tablename__, cascade='all', lazy='subquery')

        """
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = Calls(call_point_id=call_point_id, volunteer_id=volunteer_id)
                try:
                    session.add(sql)
                except Exception:
                    return False
                return True

    async def get_call_info_by_id(self, call_id: int) -> Optional[Calls]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Calls).where(or_(Calls.id == call_id))
                query = await session.execute(sql)
                return query.scalars().one_or_none()

    async def select_all_calls(self) -> Sequence[Calls]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Calls)
                query = await session.execute(sql)
                return query.scalars().all()

    async def get_calls_by_volunteer_id(self, volunteer_id: int) -> Sequence[Calls]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Calls).where(or_(Calls.volunteer_id == volunteer_id))
                query = await session.execute(sql)
                return query.scalars().all()

    async def get_calls_by_call_point_id(self, call_point_id: int) -> Sequence[Calls]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Calls).where(or_(Calls.call_point_id == call_point_id))
                query = await session.execute(sql)
                return query.scalars().all()


