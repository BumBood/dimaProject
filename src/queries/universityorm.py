from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database import session_factory
from models import University
from schemas.university_schemas import UniversityAddDTO
from schemas.university_schemas import UniversityDTO


class UniversityORM:
    @staticmethod
    async def insert_university(uni_data: UniversityAddDTO):
        async with session_factory() as session:
            try:
                uni = University(
                    name=uni_data.name,
                    url=uni_data.url
                )
                session.add(uni)
                await session.commit()
                return "Университет добавлен"
            except IntegrityError:
                await session.rollback()
                raise HTTPException(status_code=400, detail='Такой университет уже есть')

    @staticmethod
    async def get_all_universities() -> list[UniversityDTO]:
        async with session_factory() as session:
            universities = await session.execute(select(University))

        return [UniversityDTO.model_validate(_) for _ in universities]

    @staticmethod
    async def get_university(university_id: int) -> UniversityDTO:
        async with session_factory() as session:
            university = session.get_one(University, university_id)
            if not university:
                raise HTTPException(status_code=404, detail="Такого университета нет")

        return UniversityDTO.model_validate(university)
    
    @staticmethod
    async def delete_university(university_id: int):
        async with session_factory() as session:
            session.delete(University, university_id)
            await session.commit()
            return 'Универ удалён'
        
    @staticmethod
    async def update_university(university_id: int, university_data: UniversityAddDTO):   
        async with session_factory() as session:
            university= await session.get_one(University, university_id)
            university.name = university_data.name
            university.url= university_data.url
            await session.commit()
            if university is None:
                raise HTTPException(status_code=404, detail='university not found(((')
            return 'универ изменён'
        
            
