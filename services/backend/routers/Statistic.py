import os

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

import schemas
import service
from config.db import get_session
from service import get_current_user

tag = os.path.basename(__file__).split('.py')[0]
router = APIRouter(
    prefix="/api/statistics",
    tags=[tag]
)


@router.get(
    "/",
    name="Статистика"
)
async def get_order_handler(
        current_user: Annotated[schemas.User, Depends(get_current_user)],
        db: AsyncSession = Depends(get_session),

):
    return await service.get_statistic(db)
