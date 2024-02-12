import calendar
import datetime

from fastapi import HTTPException
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas


async def create_sale(sale_schema: schemas.SalesCreate, db: AsyncSession) -> schemas.Sales:
    status_res = await db.execute(select(models.SalesStatus).where(models.SalesStatus.title == 'STATUS_WAIT'))
    db_status = status_res.scalars().first()
    part_res = await db.execute(select(models.Part).where(models.Part.id == sale_schema.part_id))
    db_part = part_res.scalars().first()
    db_sale = models.Sales(
        name=sale_schema.name,
        phone=sale_schema.phone,
        count=sale_schema.count,
        part_id=sale_schema.part_id,
        total=sale_schema.count * db_part.sale_price,
        status_id=db_status.id,
        created_at=datetime.datetime.now()
    )
    db.add(db_sale)
    await db.commit()
    await db.refresh(db_sale)
    return db_sale


async def get_sales(db: AsyncSession) -> list[schemas.Sales]:
    res = await db.execute(select(models.Sales))
    sales = res.scalars().all()
    return list(sales)


async def get_sale(db: AsyncSession, sale_id: int) -> schemas.Sales or None:
    res = await db.execute(select(models.Sales).where(models.Sales.id == sale_id))
    sale = res.scalars().first()
    if not sale:
        raise HTTPException(status_code=404, detail=f"Sale with id {sale_id} not found")
    return sale


async def delete_sale(db: AsyncSession, sale_id: int) -> bool or None:
    res = await db.execute(select(models.Sales).where(models.Sales.id == sale_id))
    sale = res.scalars().first()
    if not sale:
        raise HTTPException(status_code=404, detail=f"Sale with id {sale_id} not found")
    res = await db.execute(delete(models.Sales).where(models.Sales.id == sale_id))
    await db.commit()
    return res.rowcount


async def edit_sale(db: AsyncSession, sale_schema: schemas.SalesEdit,
                    sale_id: int) -> schemas.OrderEdit or None:
    update_data = sale_schema.model_dump(exclude_unset=True)
    res = await db.execute(update(models.Sales).where(models.Sales.id == sale_id).values(update_data))
    if not res.rowcount:
        raise HTTPException(status_code=404, detail=f"Sale with id {sale_id} not found")
    await db.commit()
    res = await db.execute(select(models.Sales).where(models.Sales.id == sale_id))
    sale = res.scalars().first()
    return sale


async def get_month_sales(db: AsyncSession) -> list[schemas.StatisticDetails]:
    now = datetime.datetime.now()
    num_days = calendar.monthrange(now.year, now.month)[1]
    days = [datetime.date(now.year, now.month, day) for day in range(1, num_days + 1)]
    result = []
    for day in days:
        if datetime.date.today() < day:
            continue
        dt_min = datetime.datetime.combine(day, datetime.datetime.min.time())
        dt_max = datetime.datetime.combine(day, datetime.datetime.max.time())
        res = await db.execute(
            select(models.Sales).where(models.Sales.created_at >= dt_min, models.Sales.created_at < dt_max))
        sales = res.scalars().all()
        total = 0
        for sale in sales:
            total += sale.total
        result.append(schemas.StatisticDetails(date=day, count=len(sales), total=total))
    return result
