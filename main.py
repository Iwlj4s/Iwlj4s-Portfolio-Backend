from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from sqlalchemy.ext.asyncio import AsyncSession

from database.database import engine, Base, get_db

# from routes.user_router import user_router
from routes.admin_router import admin_router
from routes.gitgub_auth_router import auth_router
from routes.public_router import public_router
from routes.github_router import github_router
# from routes.something_router import something_router

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def startup_event():
    await create_tables()


app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(public_router)
app.include_router(github_router)


@app.get("/")
@app.get("/home")
async def home_page(db: AsyncSession = Depends(get_db)):
    return {
        "message": "It's home page",
        "status_code": 200,
        "data": {}
    }

#  uvicorn main:app --reload
