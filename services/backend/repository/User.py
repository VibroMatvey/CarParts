import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas


async def create_user(user: schemas.UserCreate, db: AsyncSession) -> schemas.User:
    salt = bcrypt.gensalt(10)
    hashed_password = bcrypt.hashpw(user.password.encode(), salt).decode('utf-8')
    db_account = models.User(
        login=user.login,
        password=hashed_password,
    )
    db.add(db_account)
    await db.commit()
    await db.refresh(db_account)
    return db_account


async def get_users(db: AsyncSession) -> list[schemas.User]:
    res = await db.execute(select(models.User))
    users = res.scalars().all()
    return list(users)
