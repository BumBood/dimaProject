from sqlalchemy import text, insert, select, func, cast, Integer, and_
from sqlalchemy.exc import IntegrityError
from src.database import engine, session_factory
from src.models import  User, University
from src.schemas.user_schemas import UserDTO, UserAddDTO
from src.schemas.university_schemas import UniversityAddDTO, UniversityDTO
from fastapi import HTTPException

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
                return 'Univer added'
            except IntegrityError as e:
                raise HTTPException(status_code=400, detail='Такой универ уже есть')