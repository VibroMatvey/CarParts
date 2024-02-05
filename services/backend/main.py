from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config.const import env
from routers import User, Token

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
app.include_router(User.router)
app.include_router(Token.router)
