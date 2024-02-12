from pydantic import BaseModel

from schemas.Part import Part
from schemas.SalesStatus import SalesStatus


class SalesCreate(BaseModel):
    name: str
    phone: str
    count: int
    part_id: int


class SalesEdit(BaseModel):
    status_id: int


class Sales(SalesCreate):
    id: int
    total: float
    part: Part
    status: SalesStatus
