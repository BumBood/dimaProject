from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from queries.universityorm import UniversityORM

from schemas.university_schemas import UniversityAddDTO, UniversityDTO

from parser.monitoring import Monitor

router_universities = APIRouter()


# @router_universities.get(
#     "/universities/update",
#     tags=["Universities"],
#     summary="Обновление статус универов на актуальные. Возвращает список универов с актуальными статусами",
# )
# async def universities_update() -> list[UniversityDTO]:
#     updated_universities = await Monitor.update_universities(await UniversityORM.get_all_universities())

#     if updated_universities:
#         return updated_universities
#     else:
#         raise HTTPException(status_code=500, detail="Произошла ошибка при сборе универов")


@router_universities.post("/universities", tags=["Universities"], summary="Регистрация нового универа")
async def reg_new_uni(uni_data: UniversityAddDTO):
    await UniversityORM.insert_university(uni_data)
    return {"ok": True, "message": "University added successfully"}


@router_universities.get("/universities", tags=["Universities"], summary="Получение всех универов")
async def get_universities() -> list[UniversityDTO]:
    unis_data = await UniversityORM.get_all_universities()
    return unis_data


@router_universities.get("/universities/{id}", tags=["Universities"], summary="Получение университета")
async def get_university(uni_id: int) -> UniversityDTO:
    unis_data = await UniversityORM.get_university(uni_id)
    return unis_data


@router_universities.put("/universities/{id}", tags=["Universities"], summary="Изменение университета")
async def update_university(uni_id: int, uni_data: UniversityAddDTO):
    await UniversityORM.update_university(uni_id, uni_data)
    return {"ok": True, "message": "University updated successfully"}


@router_universities.delete("/universities/{id}", tags=["Universities"], summary="Удаление университета")
async def delete_university(uni_id: int):
    await UniversityORM.delete_university(uni_id)
    return {"ok": True, "message": "University deleted successfully"}
