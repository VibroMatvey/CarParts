from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas


async def get_roles(db: AsyncSession) -> list[schemas.Role]:
    res = await db.execute(select(models.Role))
    roles = res.scalars().all()
    return list(roles)
