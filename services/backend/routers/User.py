import os

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

import repository
import schemas
from config.db import get_session
from service import get_current_admin, get_current_user

tag = os.path.basename(__file__).split('.py')[0]
router = APIRouter(
    prefix="/api/users",
    tags=[tag]
)


@router.post(
    "/",
    response_model=schemas.User,
    name="Создать нового пользователя"
)
async def create_user_handler(
        current_user: Annotated[schemas.User, Depends(get_current_admin)],
        user_schema: schemas.UserCreate,
        db: AsyncSession = Depends(get_session)
):
    return await repository.create_user(user_schema, db)


@router.get(
    "/",
    response_model=list[schemas.User],
    name="Получить всех пользователей"
)
async def get_users_handler(
        current_user: Annotated[schemas.User, Depends(get_current_admin)],
        db: AsyncSession = Depends(get_session)
):
    return await repository.get_users(db)


@router.get(
    "/current",
    response_model=schemas.User,
    name="Получить авторизованного пользователя"
)
async def get_current_user_handler(
        current_user: Annotated[schemas.User, Depends(get_current_user)],
):
    return current_user


@router.get(
    "/{user_id}",
    response_model=schemas.User,
    name="Получить пользователя по идентификатору"
)
async def get_user_handler(
        current_user: Annotated[schemas.User, Depends(get_current_admin)],
        user_id: int,
        db: AsyncSession = Depends(get_session),

):
    return await repository.get_user(db, user_id)


@router.delete(
    "/{user_id}",
    response_model=bool,
    name="Удалить пользователя по идентификатору"
)
async def delete_user_handler(
        current_user: Annotated[schemas.User, Depends(get_current_admin)],
        user_id: int,
        db: AsyncSession = Depends(get_session),

):
    return await repository.delete_user(db, user_id)


@router.patch(
    "/{user_id}",
    response_model=schemas.User,
    name="Редактировать пользователя по идентификатору"
)
async def edit_user_handler(
        current_user: Annotated[schemas.User, Depends(get_current_admin)],
        user_id: int,
        user_schema: schemas.UserCreate,
        db: AsyncSession = Depends(get_session),

):
    return await repository.edit_user(db, user_schema, user_id)
