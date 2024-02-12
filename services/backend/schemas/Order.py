from datetime import datetime

from pydantic import BaseModel

from schemas.OrderParts import OrderPartCreate, OrderPart
from schemas.OrderStatus import OrderStatus


class OrderCreate(BaseModel):
    parts: list[OrderPartCreate]


class OrderEdit(BaseModel):
    status_id: int


class Order(OrderCreate):
    id: int
    total: float
    parts: list[OrderPart]
    created_at: datetime
    updated_at: datetime | None = None
    status: OrderStatus
