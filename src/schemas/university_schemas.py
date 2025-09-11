from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl

from enums import AvailableStatus


class UniversityAddDTO(BaseModel):
    name: str
    url: HttpUrl


class UniversityDTO(UniversityAddDTO):
    id: int
    availability: AvailableStatus
    rating: float = Field(ge=1.0, le=5.0)

    class Config:
        from_attributes = True


if __name__ == '__main__':
    data = {
        "id": 1,
        "name": "dshdh",
        "url": "https://test.ru",
        "availability": AvailableStatus.available,
        "rating": 4
    }

    dto = UniversityDTO(**data)

    print(str(dto.url))
