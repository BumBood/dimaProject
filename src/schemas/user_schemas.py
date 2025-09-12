from pydantic import BaseModel

from schemas.review_schemas import ReviewDTO


class UserAddDTO(BaseModel):
    username: str
    password: str
    email: str


class UserDTO(UserAddDTO):
    id: int
    reviews: list['ReviewDTO']
    class Config:
        from_attributes = True
