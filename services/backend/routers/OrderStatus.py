import os

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

import repository
import schemas
from config.db import get_session
from service import get_current_user

tag = os.path.basename(__file__).split('.py')[0]
router = APIRouter(
    prefix="/api/orderStatuses",
    tags=[tag]
)


@router.get(
    "/",
    response_model=list[schemas.OrderStatus],
    name="Получить все статусы заказов"
)
async def get_order_statuses_handler(
        current_user: Annotated[schemas.User, Depends(get_current_user)],
        db: AsyncSession = Depends(get_session)
):
    return await repository.get_order_statuses(db)
