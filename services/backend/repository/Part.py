from fastapi import HTTPException
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas


async def create_part(part_schema: schemas.PartCreate, db: AsyncSession) -> schemas.Part:
    db_part = models.Part(
        title=part_schema.title,
        price=part_schema.price,
        sale_price=part_schema.sale_price,
        code=part_schema.code,
        supplier_id=part_schema.supplier_id,
    )
    db.add(db_part)
    await db.commit()
    await db.refresh(db_part)
    return db_part


async def get_parts(db: AsyncSession) -> list[schemas.Part]:
    res = await db.execute(select(models.Part))
    parts = res.scalars().all()
    return list(parts)


async def get_part(db: AsyncSession, part_id: int) -> schemas.Part or None:
    res = await db.execute(select(models.Part).where(models.Part.id == part_id))
    part = res.scalars().first()
    if not part:
        raise HTTPException(status_code=404, detail=f"Part with id {part_id} not found")
    return part


async def delete_part(db: AsyncSession, part_id: int) -> bool or None:
    res = await db.execute(select(models.Part).where(models.Part.id == part_id))
    part = res.scalars().first()
    if not part:
        raise HTTPException(status_code=404, detail=f"Part with id {part_id} not found")
    res = await db.execute(delete(models.Part).where(models.Part.id == part_id))
    await db.commit()
    return res.rowcount


async def edit_part(db: AsyncSession, part_schema: schemas.PartEdit,
                    part_id: int) -> schemas.Part or None:
    update_data = part_schema.model_dump(exclude_unset=True)
    res = await db.execute(update(models.Part).where(models.Part.id == part_id).values(update_data))
    if not res.rowcount:
        raise HTTPException(status_code=404, detail=f"Part with id {part_id} not found")
    await db.commit()
    res = await db.execute(select(models.Part).where(models.Part.id == part_id))
    part = res.scalars().first()
    return part
