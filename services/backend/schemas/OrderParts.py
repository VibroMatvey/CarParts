from pydantic import BaseModel

from schemas.Part import Part, PartCreate


class OrderPartCreate(BaseModel):
    count: int
    part_id: int


class OrderPart(OrderPartCreate):
    id: int
    part: Part
