from typing import Sequence, Optional

from sqlalchemy import select, update, or_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import DatabaseEngine
from db.models import Volunteers


class VolunteersRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def add_volunteer(self,
                            surname: str,
                            firstname: str,
                            patronymic: str,
                            email: str,
                            phone: str,
                            work_experience: str,
                            user_id: int,
                            passport_photo_id: str,
                            face_photo_id: str):
        """
        :param face_photo_id:
        :param passport_photo_id:
        :param surname: Фамилия
        :param firstname: Имя
        :param patronymic: Отчество
        :param email: почта вида fsafokas@<EMAIL>
        :param phone: 79412444242
        :param work_experience: описание
        :param user_id: алыфлафыщал
        :return:
        """
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                data = Volunteers(surname=surname,
                                  firstname=firstname,
                                  patronymic=patronymic,
                                  email=email,
                                  phone=phone,
                                  work_experience=work_experience,
                                  user_id=user_id,
                                  passport_photo_id=passport_photo_id,
                                  face_photo_id=face_photo_id)
                session.add(data)

    async def select_all_volunteers(self) -> Sequence[Volunteers]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Volunteers)
                query = await session.execute(sql)
                return query.scalars().all()

    async def select_volunteer_by_id(self, volunteer_id: int) -> Optional[Volunteers]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Volunteers).where(or_(Volunteers.id == volunteer_id))
                query = await session.execute(sql)
                return query.scalars().one_or_none()

    async def update_volunteer_status_by_volunteer_id(self, volunteer_id: int):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                volunteer = await self.select_volunteer_by_id(volunteer_id=volunteer_id)
                if volunteer:
                    sql = update(Volunteers).values({
                        Volunteers.is_active: not volunteer.is_active
                    }).where(or_(Volunteers.id == volunteer_id))
                    await session.execute(sql)
                    await session.commit()

    async def select_volunteer_by_user_id(self, user_id: int) -> Optional[Volunteers]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Volunteers).where(or_(Volunteers.user_id == user_id))
                query = await session.execute(sql)
                return query.scalars().one_or_none()
