from app.config import get_settings
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

settings = get_settings()
url_object = URL.create(
    "postgresql+psycopg",
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)

async_engine = create_async_engine(url_object)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
#AsyncSesionLocal = sessionmaker(
#    async_engine, class_=AsyncSession, expire_on_commit=False
#)

Base = declarative_base()

async def get_async_db():
    async with async_session() as db:
        yield db
        await db.commit()