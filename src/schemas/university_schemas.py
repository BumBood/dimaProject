from pydantic import BaseModel

from src.models import AvalibleStatus
class UniversityAddDTO(BaseModel):
    name: str
    
class UniversityDTO(UniversityAddDTO):
    id: int
    availability: AvalibleStatus
    rating: int# ЗДЕСь ТОТ ЖЕ ЧТО В МОДЕЛС
    class Config:
        from_attributes = True