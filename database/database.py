from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv

from config import settings

load_dotenv()

SQLALCHEMY_DB_URL = settings.DATABASE_URL

engine = create_async_engine(url=SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def get_db():
    async with SessionLocal() as db:
        try:
            yield db

        finally:
            await db.close()

SYNC_DB_URL = settings.DATABASE_URL_FOR_ALEMBIC
sync_engine = create_engine(url=SYNC_DB_URL, connect_args={"check_same_thread": False})
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

def get_sync_db():
    with SyncSessionLocal() as db:
        try:
            yield db

        finally:
            db.close()
