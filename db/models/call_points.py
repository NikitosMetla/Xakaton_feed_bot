from sqlalchemy import Column, String, Float, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship, Mapped

from db.base import BaseModel, CleanModel
from .volunteers import Volunteers

from .users import Users


class CallPoints(BaseModel, CleanModel):
    """Таблица склада волонтера"""
    __tablename__ = 'call_points'

    name_of_point = Column(String, nullable=False)
    about = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    is_active = Column(Boolean, nullable=False, default=False)

    volunteer_id = Column(Integer, ForeignKey('volunteers.id'), nullable=False)
    volunteer: Mapped[Volunteers] = relationship("Volunteers", backref=__tablename__, cascade='all', lazy='subquery')

    owner_user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    owner_user: Mapped[Users] = relationship("Users", backref=__tablename__, cascade='all', lazy='subquery')

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
