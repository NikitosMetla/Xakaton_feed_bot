from sqlalchemy import Column, BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship

from db.base import BaseModel, CleanModel
from .feed_transfers import FeedTransfers


class TransfersAlbums(BaseModel, CleanModel):
    """Альбом передачи"""
    __tablename__ = 'transfers_albums'

    photo_id = Column(String, nullable=False)

    feed_transfer_id = Column(BigInteger, ForeignKey('feed_transfers.id'), nullable=False)
    feed_transfer: Mapped[FeedTransfers] = relationship("FeedTransfers", backref=__tablename__, cascade='all', lazy='subquery')

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
