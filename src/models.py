from typing import Annotated

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from database import Base
from enums import AvailableStatus

intpk = Annotated[int, mapped_column(primary_key=True)]


class University(Base):
    __tablename__ = 'university'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)
    url: Mapped[str]
    availability: Mapped[AvailableStatus] = mapped_column(nullable=True, default=AvailableStatus.available)
    reviews: Mapped[list['Review']] = relationship(
        back_populates='university'
    )


class User(Base):
    __tablename__ = 'user'
    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    reviews: Mapped[list['Review']] = relationship(
        back_populates='user'
    )

class Review(Base):
    __tablename__='review'
    id: Mapped[intpk]
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    university_id: Mapped[int] = mapped_column(ForeignKey('university.id'))
    text: Mapped[str]
    rating: Mapped[float] = mapped_column(nullable=True)
    user: Mapped['User'] = relationship(
        back_populates='reviews'
    )
    university: Mapped['University'] = relationship(
        back_populates='reviews'
    )
    
    