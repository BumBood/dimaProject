from fastapi import APIRouter, HTTPException, status
from src.auth import Auth
from src.queries.userorm import UserORM
from src.schemas.auth_schemas import DataLoginDTO
from src.schemas.token_schemas import TokenDTO

auth_router = APIRouter()


@auth_router.post('/auth', tags=['Auth'], summary='Get access token')
async def get_auth(data_login: DataLoginDTO) -> TokenDTO:
    credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if data_login.role == 'user':
        password = await UserORM.get_password(data_login.username)
        user_id = await UserORM.get_id_by_username(data_login.username)
    else:
        raise HTTPException(status_code=409, detail='Incorrect role')
    if await Auth.verify_password(data_login.password, password):
        access_token = await Auth.create_access_token(user_id=user_id, role=data_login.role)
        return access_token
    raise credentials