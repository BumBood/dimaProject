import datetime
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, func, text, Enum, TIMESTAMP
from typing import Annotated
from sqlalchemy.testing.suite.test_reflection import metadata
from sqlalchemy.orm import  Mapped, mapped_column, relationship
import enum
from src.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]

class AvalibleStatus(enum.Enum):
    avalible= 'Доступен'
    not_avalible= 'Не доступен'

class University(Base):
    __tablename__= 'University'

    id: Mapped[intpk]
    name: Mapped[str]=mapped_column(unique=True)
    rating: Mapped[int]= mapped_column(nullable=True) #КАК ОТ 1 ДО 5 СДЕЛАТЬ
    review: Mapped[list[str]]
    availability: Mapped[AvalibleStatus]= mapped_column(nullable=True)


class User(Base):
    __tablename__ = 'user'
    id: Mapped[intpk]
    username: Mapped[str]=mapped_column(unique=True)
    password: Mapped[str]
    email= Mapped[str]=mapped_column(unique=True)
    