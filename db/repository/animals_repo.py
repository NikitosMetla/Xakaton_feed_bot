from typing import Sequence, Optional

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import DatabaseEngine
from db.models import Animals


class AnimalsRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def add_animal(self,
                         animal: str,
                         name: str,
                         breed: str,
                         gender: int,
                         latitude: float,
                         longitude: float,
                         volunteer_id: int) -> bool:
        """
            Таблица животных:
            animal - кошка собака;
            name - Зеленский;
            breed - порода;
            gender - 0 - сука 1 - кобель;
            latitude, longitude - координаты;
            volunteer_id - привязка к ид волонтеру;
            """
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                user = Animals(animal=animal,
                               name=name,
                               breed=breed,
                               gender=gender,
                               latitude=latitude,
                               longitude=longitude,
                               volunteer_id=volunteer_id)
                try:
                    session.add(user)
                except Exception:
                    return False
                return True

    async def get_animal_info_by_id(self, animal_id: int) -> Optional[Animals]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Animals).where(or_(Animals.id == animal_id))
                query = await session.execute(sql)
                return query.scalars().one_or_none()

    async def get_animals_by_volunteer_id(self, volunteer_id: int) -> Sequence[Animals]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Animals).where(or_(Animals.volunteer_id == volunteer_id))
                query = await session.execute(sql)
                return query.scalars().all()

    async def select_all_animals(self) -> Sequence[Animals]:
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Animals)
                query = await session.execute(sql)
                return query.scalars().all()
