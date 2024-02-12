import calendar
import datetime

from fastapi import HTTPException
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas


async def create_order(part_order: schemas.OrderCreate, db: AsyncSession) -> schemas.Order:
    total = 0
    order_parts = []
    res = await db.execute(select(models.OrderStatus).where(models.OrderStatus.title == 'STATUS_CREATED'))
    db_status = res.scalars().first()
    for part in part_order.parts:
        db_part_res = await db.execute(select(models.Part).where(models.Part.id == part.part_id))
        db_part = db_part_res.scalars().first()
        db_order_part = models.OrderParts(
            count=part.count,
            total=db_part.price * part.count,
            part_id=part.part_id
        )
        order_parts.append(db_order_part)
        total += db_part.price * part.count
    db_order = models.Order(
        parts=order_parts,
        total=total,
        status_id=db_status.id,
        created_at=datetime.datetime.now()
    )
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    res = await db.execute(select(models.Order).where(models.Order.id == db_order.id))
    db_order = res.scalars().first()
    return db_order


async def get_orders(db: AsyncSession) -> list[schemas.Order]:
    res = await db.execute(select(models.Order))
    orders = res.scalars().all()
    return list(orders)


async def get_order(db: AsyncSession, order_id: int) -> schemas.Order or None:
    res = await db.execute(select(models.Order).where(models.Order.id == order_id))
    order = res.scalars().first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
    return order


async def delete_order(db: AsyncSession, order_id: int) -> bool or None:
    res = await db.execute(select(models.Order).where(models.Order.id == order_id))
    order = res.scalars().first()
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
    order_part_res = await db.execute(select(models.OrderParts).where(models.OrderParts.order_id == order_id))
    order_part = order_part_res.scalars().all()
    for order_part in order_part:
        res = await db.execute(delete(models.OrderParts).where(models.OrderParts.id == order_part.id))
        await db.commit()
    res = await db.execute(delete(models.Order).where(models.Order.id == order_id))
    await db.commit()
    return res.rowcount


async def edit_order(db: AsyncSession, oder_schema: schemas.OrderEdit,
                     order_id: int) -> schemas.OrderEdit or None:
    update_data = oder_schema.model_dump(exclude_unset=True)
    res = await db.execute(update(models.Order).where(models.Order.id == order_id).values(update_data))
    if not res.rowcount:
        raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")
    await db.commit()
    res = await db.execute(select(models.Order).where(models.Order.id == order_id))
    order = res.scalars().first()
    return order


async def get_month_orders(db: AsyncSession) -> list[schemas.StatisticDetails]:
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
            select(models.Order).where(models.Order.created_at >= dt_min, models.Order.created_at < dt_max))
        orders = res.scalars().all()
        total = 0
        for order in orders:
            total += order.total
        result.append(schemas.StatisticDetails(date=day, count=len(orders), total=total))
    return result
