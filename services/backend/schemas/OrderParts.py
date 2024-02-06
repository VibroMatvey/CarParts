from pydantic import BaseModel

from schemas.Part import Part


class OrderPartCreate(BaseModel):
    count: int
    part_id: int


class OrderPart(OrderPartCreate):
    id: int
    count: int
    total: float
    part: Part
