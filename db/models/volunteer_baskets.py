from sqlalchemy import Column, Integer, BigInteger, ForeignKey, Float
from sqlalchemy.orm import Mapped, relationship

from db.base import BaseModel, CleanModel
from .feeds import Feeds
from .volunteers import Volunteers


class VolunteersBaskets(BaseModel, CleanModel):
    """Таблица склада волонтера"""
    __tablename__ = 'volunteers_baskets'

    count_feed = Column(Float, nullable=False, default=0)

    feed_id = Column(BigInteger, ForeignKey('feeds.id'), nullable=True)
    feed: Mapped[Feeds] = relationship("Feeds", backref=__tablename__, cascade='all', lazy='subquery')

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
