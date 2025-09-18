from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Header
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from src.config import settings
from src.schemas.token_schemas import TokenDataDTO, TokenDTO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

access_expires = settings.ACCESS_TOKEN_EXPIRE_MINUTES


class Auth:
    @staticmethod
    async def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    async def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    async def create_access_token(user_id: int, role: str, expires_delta: int = access_expires) -> TokenDTO:
        to_encode = {"user_id": user_id, "role": role}
        expire = datetime.now() + timedelta(minutes=expires_delta)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return TokenDTO(access_token=encoded_jwt, token_type="access")

    @staticmethod
    async def decode_access_token(token: str) -> TokenDataDTO:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("user_id")
            role = payload.get("role")
            if user_id is None or role is None:
                raise HTTPException(status_code=401, detail="Could not validate credentials")
            token_data = TokenDataDTO(user_id=user_id, role=role)
        except InvalidTokenError:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return token_data

    @staticmethod
    async def get_user_id(authorization: str = Header(...)) -> int:
        if not authorization:
            raise HTTPException(status_code=400, detail="Authorization header missing")
        type, token = authorization.split(" ")
        token_data = await Auth.decode_access_token(token)
        return int(token_data.user_id)
