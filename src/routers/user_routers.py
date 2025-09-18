from fastapi import APIRouter, Header

from src.auth import Auth
from src.queries.userorm import UserORM
from src.schemas.user_schemas import UserAddDTO, UserDTO

router_user = APIRouter()


# савв зачекай всё это особенно удаление
@router_user.post("/users", tags=["User"], summary="Регистрация нового юзера")
async def reg_new_user(user_data: UserAddDTO):
    await UserORM.insert_user(user_data)
    return {"ok": True, "message": "User added successfully"}


@router_user.get("/users/{id}", tags=["User"], summary="Получение инфы о юзере")
async def user_info(authorization: str = Header(None)):
    user_id = await Auth.get_user_id(authorization)
    return await UserORM.get_user(user_id)


@router_user.put("/users", tags=["User"], summary="Изменение информации о user")
async def update_user(user_data: UserAddDTO, authorization: str = Header(None)):
    user_id = await Auth.get_user_id(authorization)
    await UserORM.update_user(user_id, user_data)


@router_user.get("/users", tags=["User"], summary="Получение инфы о всех юзерах")
async def users_info() -> list[UserDTO]:
    users = await UserORM.get_all_user()
    return users


@router_user.delete("/users", tags=["User"], summary="Удаление юзера")
async def del_user(del_user: int):
    await UserORM.delete_user(del_user)
    return {"ok": True, "message": "User deleted successfully"}
