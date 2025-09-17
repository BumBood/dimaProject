from pydantic import BaseModel

class TokenDataDTO(BaseModel):
    user_id: str
    role: str

class TokenDTO(BaseModel):
    access_token: str
    token_type: str