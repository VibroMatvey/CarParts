from pydantic import BaseModel

from schemas.OrderParts import OrderPartCreate, OrderPart
from schemas.OrderStatus import OrderStatus


class OrderCreate(BaseModel):
    parts: list[OrderPartCreate]


class Order(OrderCreate):
    id: int
    parts: list[OrderPart]
    status: OrderStatus
