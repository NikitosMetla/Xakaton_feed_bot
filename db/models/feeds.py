from sqlalchemy import Column, String

from db.base import BaseModel, CleanModel


class Feeds(BaseModel, CleanModel):
    """Таблица кормов"""
    __tablename__ = 'feeds'

    kind_of_animal = Column(String, nullable=False)
    category_of_feed = Column(String, nullable=False)

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
