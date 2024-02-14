import os
from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import repository
import schemas
from config.db import get_session
from service import get_current_admin, get_current_user

tag = os.path.basename(__file__).split('.py')[0]
router = APIRouter(
    prefix="/api/parts",
    tags=[tag]
)


@router.post(
    "/",
    response_model=schemas.Part,
    name="Создать новую запчасть"
)
async def create_part_handler(
        current_user: Annotated[schemas.User, Depends(get_current_admin)],
        part_schema: schemas.PartCreate,
        db: AsyncSession = Depends(get_session)
):
    return await repository.create_part(part_schema, db)


@router.get(
    "/",
    response_model=list[schemas.Part],
    name="Получить все запчасти"
)
async def get_part_handler(
        db: AsyncSession = Depends(get_session)
):
    return await repository.get_parts(db)


@router.get(
    "/{part_id}",
    response_model=schemas.Part,
    name="Получить запчасть по идентификатору"
)
async def get_part_handler(
        current_user: Annotated[schemas.User, Depends(get_current_user)],
        part_id: int,
        db: AsyncSession = Depends(get_session),

):
    return await repository.get_part(db, part_id)


@router.delete(
    "/{part_id}",
    response_model=bool,
    name="Удалить запчасть по идентификатору"
)
async def delete_part_handler(
        current_user: Annotated[schemas.User, Depends(get_current_admin)],
        part_id: int,
        db: AsyncSession = Depends(get_session),

):
    return await repository.delete_part(db, part_id)


@router.patch(
    "/{part_id}",
    response_model=schemas.Part,
    name="Редактировать запчасть по идентификатору"
)
async def edit_supplier_handler(
        current_user: Annotated[schemas.User, Depends(get_current_admin)],
        part_id: int,
        part_schema: schemas.PartEdit,
        db: AsyncSession = Depends(get_session),

):
    return await repository.edit_part(db, part_schema, part_id)
