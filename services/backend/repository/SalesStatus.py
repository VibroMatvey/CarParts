from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas


async def get_sales_statuses(db: AsyncSession) -> list[schemas.SalesStatus]:
    res = await db.execute(select(models.SalesStatus))
    sales_statuses = res.scalars().all()
    return list(sales_statuses)
