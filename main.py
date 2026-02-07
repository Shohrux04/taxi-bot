# main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database import init_db, close_db  # asyncpg bilan mos database.py
from handlers import routers

# Logging sozlash
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Asosiy funksiya"""
    # Bot va Dispatcher yaratish
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Handlerlarni ro'yxatdan o'tkazish
    for router in routers:
        dp.include_router(router)
    
    # Database'ni ishga tushirish (asyncpg bilan)
    try:
        await init_db()
    except Exception as e:
        logger.error(f"❌ Database bilan ulanib bo'lmadi: {e}")
        return  # Agar database ishlamasa botni ishga tushirmaymiz
    
    logger.info("🚀 Bot ishga tushdi!")
    
    try:
        # Botni ishga tushirish (polling)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"❌ Bot ishlashida xato: {e}")
    finally:
        # Tugaganda database'ni yopish
        await close_db()
        await bot.session.close()
        logger.info("❌ Bot to'xtatildi")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⚠️ Bot foydalanuvchi tomonidan to'xtatildi")
