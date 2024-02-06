from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas


async def get_order_statuses(db: AsyncSession) -> list[schemas.OrderStatus]:
    res = await db.execute(select(models.OrderStatus))
    order_statuses = res.scalars().all()
    return list(order_statuses)
