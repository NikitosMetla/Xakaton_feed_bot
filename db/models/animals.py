

from sqlalchemy import Column, BigInteger, ForeignKey, String, Float
from sqlalchemy.orm import Mapped, relationship

from db.base import BaseModel, CleanModel
from .volunteers import Volunteers


class Animals(BaseModel, CleanModel):
    """
    Таблица животных:
    animal - кошка собака;
    name - Моська;
    breed - порода;
    gender - 0 - сука 1 - кобель;
    latitude, longitude - координаты;
    volunteer_id - привязка к ид волонтеру;
    """
    __tablename__ = 'animals'

    animal = Column(String, nullable=False)
    name = Column(String, nullable=False)
    breed = Column(String, nullable=False)
    gender = Column(BigInteger, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    volunteer_id = Column(BigInteger, ForeignKey('volunteers.id'), nullable=False)
    volunteer: Mapped[Volunteers] = relationship("Volunteers", backref=__tablename__, cascade='all', lazy='subquery')

    @property
    def stats(self) -> str:
        """
        :return:
        """
        return ""

    def __str__(self) -> str:
        return f"<{self.__tablename__}:{self.volunteer_id}>"

    def __repr__(self):
        return self.__str__()
