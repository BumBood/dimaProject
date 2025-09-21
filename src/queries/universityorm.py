
from fastapi import HTTPException
from sqlalchemy import Sequence, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from database import session_factory
from models import University
from parser.monitoring import Monitor
from schemas.university_schemas import UniversityAddDTO
from schemas.university_schemas import UniversityDTO


class UniversityORM:
    @staticmethod
    async def insert_university(uni_data: UniversityAddDTO):
        async with session_factory() as session:
            try:
                uni = University(name=uni_data.name, url=str(uni_data.url))
                session.add(uni)
                await session.commit()
                return "Университет добавлен"
            except IntegrityError:
                await session.rollback()
                raise HTTPException(status_code=400, detail="Такой университет уже есть")

    @staticmethod
    async def get_all_universities() -> list[UniversityDTO]:
        async with session_factory() as session:
            query=select(University).options(selectinload(University.reviews))
            universities = await session.execute(query)
            res=universities.scalars().all()
            return [UniversityDTO.model_validate(_) for _ in res]

    @staticmethod
    async def get_university(university_id: int) -> UniversityDTO:
        async with session_factory() as session:
            
            university = (await session.execute(select(University)
                .options(selectinload(University.reviews))
                .filter(University.id == university_id))).scalar_one_or_none()
            if not university:
                raise HTTPException(status_code=404, detail="Такого университета нет")

        return UniversityDTO.model_validate(university)

    @staticmethod
    async def delete_university(university_id: int):
        async with session_factory() as session:
            await session.delete(await session.get(University, university_id))

            await session.commit()

            return "Универ удалён"

    @staticmethod
    async def update_university(university_id: int, university_data: UniversityAddDTO):
        async with session_factory() as session:
            university = await session.get_one(University, university_id)

            university.name = university_data.name
            university.url = str(university_data.url)

            await session.commit()

            if university is None:
                raise HTTPException(status_code=404, detail="university not found(((")
            return "универ изменён"
    @staticmethod
    async def universities_update() -> list[UniversityDTO]:
        updated_universities = await Monitor.update_universities(await UniversityORM.get_all_universities())

        if updated_universities:
            return updated_universities
        else:
            raise HTTPException(status_code=500, detail="Произошла ошибка при сборе универов")