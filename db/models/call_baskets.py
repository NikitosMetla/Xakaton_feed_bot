from sqlalchemy import Column, BigInteger, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship, Mapped

from db.base import BaseModel, CleanModel
from .call_points import CallPoints
from .feeds import Feeds


class CallsBaskets(BaseModel, CleanModel):
    """Таблица склада волонтера"""
    __tablename__ = 'calls_baskets'

    count_feed = Column(Float, nullable=False, default=0)

    call_id = Column(BigInteger, ForeignKey('calls.id'), nullable=False)
    call: Mapped[CallPoints] = relationship("Calls", backref=__tablename__, cascade='all', lazy='subquery')

    feed_id = Column(BigInteger, ForeignKey('feeds.id'), nullable=False)
    feed: Mapped[Feeds] = relationship("Feeds", backref=__tablename__, cascade='all', lazy='subquery')

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
