from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from queries.universityorm import UniversityORM

from schemas.university_schemas import UniversityDTO

from parser.monitoring import Monitor

router_universities = APIRouter()

@router_universities.get("/universities/update", tags=["Universities"], summary="Обновление статус универов на актуальные. Возвращает список универов с актуальными статусами")
async def universities_update() -> list[UniversityDTO]:
    updated_universities = await Monitor.update_universities(await UniversityORM.get_all_universities())

    if updated_universities:
        return updated_universities
    else:
        raise HTTPException(status_code=500, detail="Произошла ошибка при сборе универов")