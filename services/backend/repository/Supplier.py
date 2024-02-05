from fastapi import HTTPException
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas


async def create_supplier(supplier_schema: schemas.SupplierCreate, db: AsyncSession) -> schemas.Supplier:
    db_supplier = models.Supplier(
        title=supplier_schema.title,
        address=supplier_schema.address,
        email=supplier_schema.email,
        phone=supplier_schema.phone,
    )
    db.add(db_supplier)
    await db.commit()
    await db.refresh(db_supplier)
    return db_supplier


async def get_suppliers(db: AsyncSession) -> list[schemas.Supplier]:
    res = await db.execute(select(models.Supplier))
    suppliers = res.scalars().all()
    return list(suppliers)


async def get_supplier(db: AsyncSession, supplier_id: int) -> schemas.Supplier or None:
    res = await db.execute(select(models.Supplier).where(models.Supplier.id == supplier_id))
    supplier = res.scalars().first()
    if not supplier:
        raise HTTPException(status_code=404, detail=f"Supplier with id {supplier_id} not found")
    return supplier


async def delete_supplier(db: AsyncSession, supplier_id: int) -> bool or None:
    res = await db.execute(select(models.Supplier).where(models.Supplier.id == supplier_id))
    supplier = res.scalars().first()
    if not supplier:
        raise HTTPException(status_code=404, detail=f"Supplier with id {supplier_id} not found")
    res = await db.execute(delete(models.Supplier).where(models.Supplier.id == supplier_id))
    await db.commit()
    return res.rowcount


async def edit_supplier(db: AsyncSession, supplier_schema: schemas.SupplierEdit,
                        supplier_id: int) -> schemas.Supplier or None:
    update_data = supplier_schema.model_dump(exclude_unset=True)
    res = await db.execute(update(models.Supplier).where(models.Supplier.id == supplier_id).values(update_data))
    if not res.rowcount:
        raise HTTPException(status_code=404, detail=f"Supplier with id {supplier_id} not found")
    await db.commit()
    res = await db.execute(select(models.Supplier).where(models.Supplier.id == supplier_id))
    supplier = res.scalars().first()
    return supplier
