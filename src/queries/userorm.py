from sqlalchemy import text, insert, select, func, cast, Integer, and_
from sqlalchemy.exc import IntegrityError
from src.database import engine, session_factory
from src.models import Order, User, Pizza,OrderPizza
from src.schemas.user_schemas import UserDTO, UserAddDTO
from fastapi import HTTPException

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
                return'user added'
            except IntegrityError as e:
                raise HTTPException(status_code=400, detail='Такой пользователь уже есть')

            