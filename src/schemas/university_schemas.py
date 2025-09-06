from pydantic import BaseModel
from pydantic import Field

from src.enums import AvailableStatus


class UniversityAddDTO(BaseModel):
    name: str


class UniversityDTO(UniversityAddDTO):
    id: int
    availability: AvailableStatus
    rating: float = Field(ge=1.0, le=5.0)

    class Config:
        from_attributes = True

# if __name__ == '__main__':
#     data = {
#         "id": 1,
#         "name": "dshdh",
#         "availability": AvailableStatus.available,
#         "rating": 4
#     }
#     print(UniversityDTO(**data))
