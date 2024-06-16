from sqlalchemy import Column, BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship

from db.base import BaseModel, CleanModel
from .calls import Calls


class ReceivingAlbums(BaseModel, CleanModel):
    """Альбом передачи"""
    __tablename__ = 'receivings_albums'

    photo_id = Column(String, nullable=False)

    call_id = Column(BigInteger, ForeignKey('calls.id'), nullable=False)
    call: Mapped[Calls] = relationship("Calls", backref=__tablename__, cascade='all', lazy='subquery')

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
