from pydantic import BaseModel, EmailStr


class SHolders(BaseModel):
    username: str
    password: str
    email: EmailStr
    age: int


class SHoldersAuth(BaseModel):
    email: EmailStr
    password: str
