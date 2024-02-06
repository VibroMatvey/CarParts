import os
from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import repository
import schemas
from config.db import get_session
from service import get_current_user, get_current_admin

tag = os.path.basename(__file__).split('.py')[0]
router = APIRouter(
    prefix="/api/orders",
    tags=[tag]
)


@router.post(
    "/",
    response_model=schemas.Order,
    name="Создать новый заказ"
)
async def create_order_handler(
        current_user: Annotated[schemas.User, Depends(get_current_user)],
        order_schema: schemas.OrderCreate,
        db: AsyncSession = Depends(get_session)
):
    return await repository.create_order(order_schema, db)


@router.get(
    "/",
    response_model=list[schemas.Order],
    name="Получить все заказы"
)
async def get_order_handler(
        current_user: Annotated[schemas.User, Depends(get_current_user)],
        db: AsyncSession = Depends(get_session)
):
    return await repository.get_orders(db)


@router.get(
    "/{order_id}",
    response_model=schemas.Order,
    name="Получить заказ по идентификатору"
)
async def get_order_handler(
        current_user: Annotated[schemas.User, Depends(get_current_user)],
        order_id: int,
        db: AsyncSession = Depends(get_session),

):
    return await repository.get_order(db, order_id)


@router.delete(
    "/{order_id}",
    response_model=bool,
    name="Удалить заказ по идентификатору"
)
async def delete_order_handler(
        current_user: Annotated[schemas.User, Depends(get_current_user)],
        order_id: int,
        db: AsyncSession = Depends(get_session),

):
    return await repository.delete_order(db, order_id)


@router.patch(
    "/{order_id}",
    response_model=schemas.Order,
    name="Редактировать заказ по идентификатору"
)
async def edit_supplier_handler(
        current_user: Annotated[schemas.User, Depends(get_current_admin)],
        order_id: int,
        order_schema: schemas.OrderEdit,
        db: AsyncSession = Depends(get_session),

):
    return await repository.edit_order(db, order_schema, order_id)
