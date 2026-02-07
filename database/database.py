# database.py
import os
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# .env fayldan sozlamalarni yuklash
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  # asyncpg bilan URL bo'lishi kerak
if not DATABASE_URL:
    raise ValueError("DATABASE_URL topilmadi! .env faylini tekshiring.")

# Logging sozlash
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Async engine yaratish
engine = create_async_engine(DATABASE_URL, echo=True)

# Async session factory
async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Base model
Base = declarative_base()

async def init_db():
    """Database'ni ishga tushirish va table'larni yaratish"""
    async with engine.begin() as conn:
        logger.info("🟢 Database bilan ulanish boshlanmoqda...")
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Database initialized")

async def close_db():
    """Database'ni yopish"""
    await engine.dispose()
    logger.info("✅ Database closed")
