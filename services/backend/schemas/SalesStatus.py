from pydantic import BaseModel


class SalesStatus(BaseModel):
    id: int
    title: str
