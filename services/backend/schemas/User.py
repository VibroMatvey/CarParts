from pydantic import BaseModel

from schemas.Role import Role


class User(BaseModel):
    id: int
    login: str
    role: Role


class UserCreate(BaseModel):
    login: str
    password: str
    role_id: int
