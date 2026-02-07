import asyncpg
from config import DATABASE_URL
from database.models import INIT_DB

pool = None

async def init_db():
    """Ma'lumotlar bazasini ishga tushirish"""
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)
    
    async with pool.acquire() as conn:
        for query in INIT_DB:
            await conn.execute(query)
    
    print("✅ Database muvaffaqiyatli ishga tushdi!")

async def close_db():
    """Ma'lumotlar bazasini yopish"""
    global pool
    if pool:
        await pool.close()
        print("❌ Database yopildi")

def get_pool():
    """Connection pool olish"""
    return pool