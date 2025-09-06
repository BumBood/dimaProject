from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from src.database import session_factory
from src.models import User
from src.schemas.user_schemas import UserAddDTO


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
