from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl
from schemas.review_schemas import ReviewDTO
from enums import AvailableStatus


class UniversityAddDTO(BaseModel):
    name: str
    url: HttpUrl
class UniversityDTO(UniversityAddDTO):
    id: int
    availability: AvailableStatus
    reviews: list[ReviewDTO]
    

    class Config:
        from_attributes = True



