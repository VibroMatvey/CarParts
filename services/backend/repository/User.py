import bcrypt
from fastapi import HTTPException
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas


async def create_user(user_schema: schemas.UserCreate, db: AsyncSession) -> schemas.User:
    existing_user_res = await db.execute(select(models.User).where(models.User.login == user_schema.login))
    existing_user = existing_user_res.scalars().first()
    if existing_user:
        raise HTTPException(status_code=422, detail=f"User with login {user_schema.login} already exist")
    salt = bcrypt.gensalt(10)
    hashed_password = bcrypt.hashpw(user_schema.password.encode(), salt).decode('utf-8')
    db_account = models.User(
        login=user_schema.login,
        password=hashed_password,
        role_id=user_schema.role_id
    )
    db.add(db_account)
    await db.commit()
    await db.refresh(db_account)
    return db_account


async def get_users(db: AsyncSession) -> list[schemas.User]:
    res = await db.execute(select(models.User))
    users = res.scalars().all()
    return list(users)


async def get_user(db: AsyncSession, user_id: int) -> schemas.User or None:
    res = await db.execute(select(models.User).where(models.User.id == user_id))
    user = res.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return user


async def delete_user(db: AsyncSession, user_id: int) -> bool or None:
    res = await db.execute(select(models.User).where(models.User.id == user_id))
    user = res.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    res = await db.execute(delete(models.User).where(models.User.id == user_id))
    await db.commit()
    return res.rowcount


async def edit_user(db: AsyncSession, user_schema: schemas.UserCreate, user_id: int) -> schemas.User or None:
    update_data = user_schema.model_dump(exclude_unset=True)
    res = await db.execute(update(models.User).where(models.User.id == user_id).values(update_data))
    if not res.rowcount:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    await db.commit()
    res = await db.execute(select(models.User).where(models.User.id == user_id))
    user = res.scalars().first()
    return user
