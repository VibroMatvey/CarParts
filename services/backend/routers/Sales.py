import os

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

import repository
import schemas
from config.db import get_session
from service import get_current_user, get_current_admin

tag = os.path.basename(__file__).split('.py')[0]
router = APIRouter(
    prefix="/api/sales",
    tags=[tag]
)


@router.post(
    "/",
    response_model=schemas.Sales,
    name="Создать новую продажу"
)
async def create_order_handler(
        sales_schema: schemas.SalesCreate,
        db: AsyncSession = Depends(get_session)
):
    return await repository.create_sale(sales_schema, db)


@router.get(
    "/",
    response_model=list[schemas.Sales],
    name="Получить все продажи"
)
async def get_order_handler(
        current_user: Annotated[schemas.User, Depends(get_current_user)],
        db: AsyncSession = Depends(get_session)
):
    return await repository.get_sales(db)


@router.get(
    "/{sale_id}",
    response_model=schemas.Sales,
    name="Получить продажу по идентификатору"
)
async def get_order_handler(
        current_user: Annotated[schemas.User, Depends(get_current_user)],
        sale_id: int,
        db: AsyncSession = Depends(get_session),

):
    return await repository.get_sale(db, sale_id)


@router.delete(
    "/{sale_id}",
    response_model=bool,
    name="Удалить продажу по идентификатору"
)
async def delete_order_handler(
        current_user: Annotated[schemas.User, Depends(get_current_user)],
        sale_id: int,
        db: AsyncSession = Depends(get_session),

):
    return await repository.delete_sale(db, sale_id)


@router.patch(
    "/{sale_id}",
    response_model=schemas.Sales,
    name="Редактировать продажу по идентификатору"
)
async def edit_supplier_handler(
        current_user: Annotated[schemas.User, Depends(get_current_admin)],
        sale_id: int,
        sale_schema: schemas.SalesEdit,
        db: AsyncSession = Depends(get_session),

):
    return await repository.edit_sale(db, sale_schema, sale_id)
