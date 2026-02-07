from database import get_pool

async def create_order(client_id: int, people_count: int, address: str, 
                       price: int, direction: str, latitude: float, longitude: float):
    """Yangi buyurtma yaratish"""
    pool = get_pool()
    async with pool.acquire() as conn:
        order_id = await conn.fetchval(
            """
            INSERT INTO orders (client_id, people_count, address, price, direction, latitude, longitude)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id
            """,
            client_id, people_count, address, price, direction, latitude, longitude
        )
        return order_id

async def get_active_orders(direction: str):
    """Aktiv buyurtmalarni olish"""
    pool = get_pool()
    async with pool.acquire() as conn:
        return await conn.fetch(
            """
            SELECT o.*, u.name, u.phone 
            FROM orders o
            JOIN users u ON o.client_id = u.id
            WHERE o.direction = $1 AND o.status = 'active'
            ORDER BY o.created_at DESC
            """,
            direction
        )

async def get_order(order_id: int):
    """Buyurtmani olish"""
    pool = get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchrow(
            """
            SELECT o.*, u.name, u.phone 
            FROM orders o
            JOIN users u ON o.client_id = u.id
            WHERE o.id = $1
            """,
            order_id
        )

async def take_order(order_id: int, driver_id: int):
    """Buyurtmani olish"""
    pool = get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "UPDATE orders SET status = 'taken', driver_id = $1 WHERE id = $2",
            driver_id, order_id
        )

async def cancel_order(order_id: int):
    """Buyurtmani bekor qilish - ACTIVE holatga qaytarish"""
    pool = get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "UPDATE orders SET status = 'active', driver_id = NULL WHERE id = $1",
            order_id
        )

async def get_user_orders(user_id: int):
    """Foydalanuvchi buyurtmalarini olish"""
    pool = get_pool()
    async with pool.acquire() as conn:
        return await conn.fetch(
            """
            SELECT * FROM orders 
            WHERE client_id = $1 OR driver_id = $1
            ORDER BY created_at DESC
            LIMIT 10
            """,
            user_id
        )

async def get_driver_active_orders(driver_id: int):
    """Haydovchi olingan buyurtmalari"""
    pool = get_pool()
    async with pool.acquire() as conn:
        return await conn.fetch(
            """
            SELECT o.*, u.name, u.phone 
            FROM orders o
            JOIN users u ON o.client_id = u.id
            WHERE o.driver_id = $1 AND o.status = 'taken'
            ORDER BY o.created_at DESC
            """,
            driver_id
        )
