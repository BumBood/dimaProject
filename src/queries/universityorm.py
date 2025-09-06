from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from src.database import session_factory
from src.models import University
from src.schemas.university_schemas import UniversityAddDTO


class UniversityORM:
    @staticmethod
    async def insert_university(uni_data: UniversityAddDTO):
        async with session_factory() as session:
            try:
                uni = University(
                    name=uni_data.name,
                )
                session.add(uni)
                await session.commit()
                return "Университет добавлен"
            except IntegrityError as e:
                await session.rollback()
                raise HTTPException(status_code=400, detail='Такой универ уже есть')
