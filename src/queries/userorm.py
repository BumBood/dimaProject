from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.database import session_factory
from src.models import User
from src.schemas.user_schemas import UserAddDTO, UserDTO


class UserORM:
    @staticmethod
    async def insert_user(user_data: UserAddDTO):
        async with session_factory() as session:
            try:
                user = User(
                    username=user_data.username,
                    password=user_data.password,
                    email=user_data.email
                )
                session.add(user)
                await session.commit()
                return "Пользователь добавлен"
            except IntegrityError as e:
                raise HTTPException(status_code=400, detail='Такой пользователь уже есть')
    
    @staticmethod
    async def get_all_user() -> list[UserDTO]:
        async with session_factory() as session:
            user = await session.execute(select(User))

        return [UserDTO.model_validate(_) for _ in user]

    @staticmethod
    async def get_user(user_id: int) -> UserDTO:
        async with session_factory() as session:
            user = session.get_one(User, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="Такого пользователя нет")

        return UserDTO.model_validate(user)
    
    @staticmethod
    async def delete_user(user_id: int):
        async with session_factory() as session:
            await session.delete(await session.get(User, user_id))
            await session.commit()
            return 'Юзер удалён'
        
    @staticmethod
    async def update_user(user_id: int, user_data: UserAddDTO):   
        async with session_factory() as session:
            user= await session.get_one(User, user_id)
            user.username = user_data.username
            user.password= user_data.password
            user.email=user_data.email
            await session.commit()
            if user is None:
                raise HTTPException(status_code=404, detail='user not found(((')
            return 'Юзер изменён'
        