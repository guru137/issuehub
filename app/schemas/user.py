from pydantic import BaseModel
from pydantic import EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=6)



class UserLogin(BaseModel):
    email: str
    password: str
