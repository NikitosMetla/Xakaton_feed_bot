from sqlalchemy import Column, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from db.base import BaseModel, CleanModel
from .call_points import CallPoints
from .users import Users


class FeedTransfers(BaseModel, CleanModel):
    """Таблица склада волонтера"""
    __tablename__ = 'feed_transfers'

    # latitude = Column(Float, nullable=False)
    # longitude = Column(Float, nullable=False)

    volunteer_id = Column(BigInteger, ForeignKey('volunteers.id'), nullable=False)
    volunteer: Mapped[CallPoints] = relationship("Volunteers", backref=__tablename__, cascade='all', lazy='subquery')

    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    user: Mapped[Users] = relationship("Users", backref=__tablename__, cascade='all', lazy='subquery')
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
