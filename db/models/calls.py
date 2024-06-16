from sqlalchemy import Column, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from db.base import BaseModel, CleanModel
from .call_points import CallPoints
from .volunteers import Volunteers


class Calls(BaseModel, CleanModel):
    """Таблица склада волонтера"""
    __tablename__ = 'calls'

    call_point_id = Column(BigInteger, ForeignKey('call_points.id'), nullable=False)
    call_point: Mapped[CallPoints] = relationship("CallPoints", backref=__tablename__, cascade='all', lazy='subquery')

    volunteer_id = Column(BigInteger, ForeignKey('volunteers.id'), nullable=False)
    volunteer: Mapped[Volunteers] = relationship("Volunteers", backref=__tablename__, cascade='all', lazy='subquery')

    @property
    def stats(self) -> str:
        """
        :return:
        """
        return ""

    def __str__(self) -> str:
        return f"<{self.__tablename__}:{self.id}>"

    def __repr__(self):
        return self.__str__()
