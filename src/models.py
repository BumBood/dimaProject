from typing import Annotated

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.database import Base
from src.enums import AvailableStatus

intpk = Annotated[int, mapped_column(primary_key=True)]


class University(Base):
    __tablename__ = 'University'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)
    url: Mapped[str] = mapped_column(unique=True)
    rating: Mapped[float] = mapped_column(nullable=True)
    review: Mapped[list[str]]
    availability: Mapped[AvailableStatus] = mapped_column(nullable=True)


class User(Base):
    __tablename__ = 'user'
    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
