from database import get_pool

async def create_user(user_id: int, role: str, name: str, phone: str):
    """Yangi foydalanuvchi yaratish"""
    pool = get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO users (id, role, name, phone) VALUES ($1, $2, $3, $4)",
            user_id, role, name, phone
        )

async def get_user(user_id: int):
    """Foydalanuvchini olish"""
    pool = get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)

async def create_driver(user_id: int, car_model: str, car_number: str):
    """Haydovchi ma'lumotlarini saqlash"""
    pool = get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO drivers (user_id, car_model, car_number) VALUES ($1, $2, $3)",
            user_id, car_model, car_number
        )

async def get_driver(user_id: int):
    """Haydovchi ma'lumotlarini olish"""
    pool = get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchrow("SELECT * FROM drivers WHERE user_id = $1", user_id)