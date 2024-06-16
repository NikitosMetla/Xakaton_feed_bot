from sqlalchemy import Column, BigInteger, String

from db.base import BaseModel, CleanModel


class Users(BaseModel, CleanModel):
    """
    Таблица юзеров
    privilege_level: 0 - юзер; 1 - волонтёр; 2 - main волонтёр; 3 - админ точки; 4 - админ бота
    """
    __tablename__ = 'users'

    user_id = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    username = Column(String, nullable=True, unique=False)
    privilege_level = Column(BigInteger, nullable=False, unique=False, default=0)

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
