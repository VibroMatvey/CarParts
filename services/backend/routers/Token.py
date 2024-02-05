import os
from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
import service
from config.db import get_session

tag = os.path.basename(__file__).split('.py')[0]
router = APIRouter(tags=[tag])


@router.post(
    "/token",
    response_model=schemas.Token,
    name="Получить токен"
)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: AsyncSession = Depends(get_session)
):
    return await service.token(form_data, db)
