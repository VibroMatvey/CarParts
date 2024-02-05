import os
from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import repository
import schemas
from config.db import get_session
from service import get_current_active_user

tag = os.path.basename(__file__).split('.py')[0]
router = APIRouter(
    prefix="/users",
    tags=[tag]
)


@router.post(
    "/",
    response_model=schemas.User,
    name="Создать нового пользователя"
)
async def create_user_handler(
        user: schemas.UserCreate,
        db: AsyncSession = Depends(get_session)
):
    return await repository.create_user(user, db)


@router.get(
    "/",
    response_model=list[schemas.User],
    name="Получить всех пользователей"
)
async def get_users_handler(
        current_user: Annotated[schemas.User, Depends(get_current_active_user)],
        db: AsyncSession = Depends(get_session)
):
    return await repository.get_users(db)
