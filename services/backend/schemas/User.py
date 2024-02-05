from pydantic import BaseModel


class User(BaseModel):
    id: int
    login: str
    password: str


class UserCreate(BaseModel):
    login: str
    password: str
