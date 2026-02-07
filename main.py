# main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database import init_db, close_db
from handlers import routers

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    for router in routers:
        dp.include_router(router)

    try:
        await init_db()
    except Exception as e:
        logger.error(f"❌ Database bilan ulanib bo‘lmadi: {e}")
        return

    logger.info("🚀 Bot ishga tushdi!")

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"❌ Bot ishlashida xato: {e}")
    finally:
        await close_db()
        await bot.session.close()
        logger.info("❌ Bot to‘xtatildi")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⚠️ Bot foydalanuvchi tomonidan to‘xtatildi")
