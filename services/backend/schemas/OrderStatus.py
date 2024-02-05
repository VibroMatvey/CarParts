from pydantic import BaseModel

from schemas.OrderParts import OrderPartCreate, OrderPart


class OrderStatus(BaseModel):
    id: int
    title: str
