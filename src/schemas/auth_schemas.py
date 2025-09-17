from pydantic import BaseModel

class DataLoginDTO(BaseModel):
    email: str
    username: str
    password: str
    role: str