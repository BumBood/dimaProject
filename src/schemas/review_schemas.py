from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl

class ReviewAddDTO(BaseModel):
    author_id: int
    university_id: int
    text: str 
    rating: int = Field(ge=1, le=5)

class ReviewDTO(ReviewAddDTO):
    id: int 
    
class Config:
        from_attributes = True