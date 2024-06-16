from typing import Sequence, Optional

from sqlalchemy import select, or_, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import DatabaseEngine
from db.models import CallPoints


class CallPointsRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def add_call_point(self,
                             name_of_point: str,
                             about: str,
                             phone: str,
                             latitude: float,
                             longitude: float,
                             volunteer_id: int,
                             owner_user_id: int):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                point = CallPoints(name_of_point=name_of_point,
                                   about=about,
                                   phone=phone,
                                   latitude=latitude,
                                   longitude=longitude,
                                   volunteer_id=volunteer_id,
                                   owner_user_id=owner_user_id)
                try:
                    session.add(point)
                except Exception:
                    return False
                return True

    async def select_all_points(self) -> Sequence[CallPoints]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(CallPoints)
                query = await session.execute(sql)
                return query.scalars().all()

    async def get_call_point_by_id(self, call_point_id: int) -> Optional[CallPoints]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(CallPoints).where(or_(CallPoints.id == call_point_id))
                query = await session.execute(sql)
                return query.scalars().one_or_none()

    async def get_call_points_by_owner_user_id(self, owner_user_id: int) -> Sequence[CallPoints]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(CallPoints).where(or_(CallPoints.owner_user_id == owner_user_id))
                query = await session.execute(sql)
                return query.scalars().all()

    async def get_call_points_by_volunteer_id(self, volunteer_id: int) -> Sequence[CallPoints]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(CallPoints).where(or_(CallPoints.volunteer_id == volunteer_id))
                query = await session.execute(sql)
                return query.scalars().all()

    async def update_call_point_status_by_id(self, call_point_id: int):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                call_point = await self.get_call_point_by_id(call_point_id=call_point_id)
                if call_point:
                    sql = update(CallPoints).values({
                        CallPoints.is_active: not call_point.is_active
                    }).where(or_(CallPoints.id == call_point_id))
                    await session.execute(sql)
                    await session.commit()
