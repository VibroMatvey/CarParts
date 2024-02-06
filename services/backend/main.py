from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select

import models
from config.const import env
from config.db import async_session
from routers import User, Token, Role, Supplier, Part, Order, OrderStatus

docs = '/api'

if env['APP_ENV'] == 'prod':
    docs = None

app = FastAPI(docs_url=docs, redoc_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(Token.router)
app.include_router(Role.router)
app.include_router(OrderStatus.router)
app.include_router(User.router)
app.include_router(Supplier.router)
app.include_router(Part.router)
app.include_router(Order.router)


@app.on_event('startup')
async def startup_event():
    db = async_session()
    roles = ["ROLE_ADMIN", "ROLE_USER"]
    statuses = ["STATUS_CREATED", "STATUS_TRANSIT", "STATUS_DONE"]
    users = ["admin", "user"]
    for role in roles:
        res = await db.execute(select(models.Role).where(models.Role.title == role))
        db_role = res.scalars().first()
        if not db_role:
            db_role = models.Role(
                title=role
            )
            db.add(db_role)
            await db.commit()
            await db.refresh(db_role)
    for status in statuses:
        res = await db.execute(select(models.OrderStatus).where(models.OrderStatus.title == status))
        db_status = res.scalars().first()
        if not db_status:
            db_status = models.OrderStatus(
                title=status
            )
            db.add(db_status)
            await db.commit()
            await db.refresh(db_status)
    for user in users:
        role_user = 2
        if user == "admin":
            role_user = 1
        res = await db.execute(select(models.User).where(models.User.login == user))
        db_user = res.scalars().first()
        if not db_user:
            db_user = models.User(
                login=user,
                password='$2a$10$OeJdUH5KtliQljc91sQMIOOIkQ/MSRMvP9oLmH5MA8R02MBvYf6be',
                role_id=role_user
            )
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
