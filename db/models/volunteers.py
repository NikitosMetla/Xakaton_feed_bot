from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, FetchedValue, Boolean
from sqlalchemy.orm import Mapped, relationship

from db.base import BaseModel, CleanModel
from .users import Users


class Volunteers(BaseModel, CleanModel):
    """Таблица юзеров"""
    __tablename__ = 'volunteers'

    surname = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    work_experience = Column(String, nullable=False)
    passport_photo_id = Column(String, nullable=False)
    face_photo_id = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)

    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False, unique=True)
    user: Mapped[Users] = relationship("Users", backref=__tablename__, cascade='all', lazy='subquery')

    @property
    def stats(self) -> str:
        """
        :return:
        """
        return ""

    def __str__(self) -> str:
        return f"<{self.__tablename__}:{self.user_id}>"

    def __repr__(self):
        return self.__str__()
