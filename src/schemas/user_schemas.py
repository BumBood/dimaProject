from pydantic import BaseModel


class UserAddDTO(BaseModel):
    username: str
    password: str
    email: str


class UserDTO(UserAddDTO):
    id: int

    class Config:
        from_attributes = True
