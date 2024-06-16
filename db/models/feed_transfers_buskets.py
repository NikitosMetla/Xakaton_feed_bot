from sqlalchemy import Column, BigInteger, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship, Mapped

from db.base import BaseModel, CleanModel
from .feed_transfers import FeedTransfers
from .feeds import Feeds


class FeedTransfersBuskets(BaseModel, CleanModel):
    """Таблица склада волонтера"""
    __tablename__ = 'feed_transfers_buskets'

    count_feed = Column(Float, nullable=False, default=0)

    feed_id = Column(BigInteger, ForeignKey('feeds.id'), nullable=True)
    feed: Mapped[Feeds] = relationship("Feeds", backref=__tablename__, cascade='all', lazy='subquery')

    feed_transfer_id = Column(BigInteger, ForeignKey('feed_transfers.id'), nullable=False)
    feed_transfer: Mapped[FeedTransfers] = relationship("FeedTransfers", backref=__tablename__, cascade='all',
                                                        lazy='subquery')

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
