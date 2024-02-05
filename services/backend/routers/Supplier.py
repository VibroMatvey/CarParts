import os

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

import repository
import schemas
from config.db import get_session
from service import get_current_admin

tag = os.path.basename(__file__).split('.py')[0]
router = APIRouter(
    prefix="/api/suppliers",
    tags=[tag]
)


@router.post(
    "/",
    response_model=schemas.Supplier,
    name="Создать нового поставщика"
)
async def create_supplier_handler(
        current_user: Annotated[schemas.User, Depends(get_current_admin)],
        supplier_schema: schemas.SupplierCreate,
        db: AsyncSession = Depends(get_session)
):
    return await repository.create_supplier(supplier_schema, db)


@router.get(
    "/",
    response_model=list[schemas.Supplier],
    name="Получить всех поставщиков"
)
async def get_supplier_handler(
        current_user: Annotated[schemas.User, Depends(get_current_admin)],
        db: AsyncSession = Depends(get_session)
):
    return await repository.get_suppliers(db)


@router.get(
    "/{supplier_id}",
    response_model=schemas.Supplier,
    name="Получить поставщика по идентификатору"
)
async def get_supplier_handler(
        current_user: Annotated[schemas.User, Depends(get_current_admin)],
        supplier_id: int,
        db: AsyncSession = Depends(get_session),

):
    return await repository.get_supplier(db, supplier_id)


@router.delete(
    "/{supplier_id}",
    response_model=bool,
    name="Удалить поставщика по идентификатору"
)
async def delete_supplier_handler(
        current_user: Annotated[schemas.User, Depends(get_current_admin)],
        supplier_id: int,
        db: AsyncSession = Depends(get_session),

):
    return await repository.delete_supplier(db, supplier_id)


@router.patch(
    "/{supplier_id}",
    response_model=schemas.Supplier,
    name="Редактировать поставщика по идентификатору"
)
async def edit_supplier_handler(
        current_user: Annotated[schemas.User, Depends(get_current_admin)],
        supplier_id: int,
        supplier_schema: schemas.SupplierEdit,
        db: AsyncSession = Depends(get_session),

):
    return await repository.edit_supplier(db, supplier_schema, supplier_id)
