from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

# from src.databases.sqlite_database import init_db
from src.databases.pg_database import engine, Base
from src.routes import auth_routes, todo_routes

# @asynccontextmanager
# async def lifespan(_: FastAPI):
#     await init_db()
#     yield

@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# api routes
app.include_router(auth_routes.router)
app.include_router(todo_routes.router)
