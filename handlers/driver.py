from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery

from config import BOT_TOKEN
from keyboards.inline import (
    get_direction_filter_keyboard,
    get_order_action_keyboard,
    get_cancel_order_keyboard
)
from keyboards.reply import get_main_menu_driver
from services.order_service import (
    get_active_orders,
    get_order,
    take_order,
    cancel_order,
    get_driver_active_orders
)
from services.user_service import get_user, get_driver

router = Router()

# BUYURTMALAR RO'YXATI
@router.message(F.text == "📋 Buyurtmalar ro'yxati")
async def orders_list(message: Message):
    """Yo'nalish tanlash"""
    await message.answer(
        "🔄 Yo'nalishni tanlang:",
        reply_markup=get_direction_filter_keyboard()
    )

# YO'NALISH BO'YICHA BUYURTMALAR
@router.callback_query(F.data.startswith("filter_"))
async def show_orders_by_direction(callback: CallbackQuery):
    """Yo'nalish bo'yicha buyurtmalarni ko'rsatish"""
    direction = callback.data.split("filter_")[1]
    orders = await get_active_orders(direction)
    
    direction_text = "🔵 Mangit → Nukus" if direction == "mangit_nukus" else "🔴 Nukus → Mangit"
    
    if not orders:
        await callback.message.edit_text(
            f"❌ {direction_text} yo'nalishida aktiv buyurtmalar yo'q"
        )
        return
    
    await callback.message.edit_text(f"📋 Aktiv buyurtmalar ({direction_text}):")
    
    for order in orders:
        order_text = (
            f"🆔 Buyurtma #{order['id']}\n\n"
            f"👤 Mijoz: {order['name']}\n"
            f"📱 Telefon: {order['phone']}\n"
            f"👥 Odam soni: {order['people_count']}\n"
            f"📍 Manzil: {order['address']}\n"
            f"💰 Narx (1 kishi): {order['price']:,} so'm\n"
            f"💵 Jami: {order['price'] * order['people_count']:,} so'm\n"
            f"📍 Lokatsiya: {order['latitude']:.6f}, {order['longitude']:.6f}\n"
            f"📅 {order['created_at'].strftime('%d.%m.%Y %H:%M')}"
        )
        
        await callback.message.answer(
            order_text,
            reply_markup=get_order_action_keyboard(order['id'])
        )

# BUYURTMANI OLISH
@router.callback_query(F.data.startswith("take_order_"))
async def take_order_handler(callback: CallbackQuery):
    """Buyurtmani olish va mijozga xabar yuborish"""
    bot = Bot(token=BOT_TOKEN)
    order_id = int(callback.data.split("take_order_")[1])
    driver_id = callback.from_user.id
    
    # Buyurtmani olish
    await take_order(order_id, driver_id)
    
    # Buyurtma ma'lumotlarini olish
    order = await get_order(order_id)
    
    # Haydovchi ma'lumotlarini olish
    driver_user_info = await get_user(driver_id)
    driver_info = await get_driver(driver_id)
    
    # Haydovchiga xabar
    await callback.message.edit_text(
        f"✅ Buyurtma #{order_id} qabul qilindi!\n\n"
        f"👤 Mijoz: {order['name']}\n"
        f"📱 Telefon: {order['phone']}\n"
        f"📍 Manzil: {order['address']}\n"
        f"👥 Odam soni: {order['people_count']}\n"
        f"💰 Narx: {order['price'] * order['people_count']:,} so'm\n\n"
        f"📍 Lokatsiya:\n"
        f"https://www.google.com/maps?q={order['latitude']},{order['longitude']}",
        reply_markup=get_cancel_order_keyboard(order_id)
    )
    
    # Mijozga haydovchi haqida xabar yuborish
    client_message = (
        f"✅ Sizning buyurtmangiz #{order_id} qabul qilindi!\n\n"
        f"🚗 Haydovchi ma'lumotlari:\n\n"
        f"👤 Ism: {driver_user_info['name']}\n"
        f"📱 Telefon: {driver_user_info['phone']}\n"
        f"🚗 Mashina: {driver_info['car_model']}\n"
        f"🔢 Raqam: {driver_info['car_number']}\n\n"
        f"Haydovchi tez orada siz bilan bog'lanadi!"
    )
    
    try:
        await bot.send_message(
            chat_id=order['client_id'],
            text=client_message
        )
    except Exception as e:
        print(f"❌ Mijozga xabar yuborishda xatolik: {e}")
    
    await bot.session.close()

# BUYURTMANI BEKOR QILISH
@router.callback_query(F.data.startswith("cancel_taken_"))
async def cancel_taken_order(callback: CallbackQuery):
    """Olingan buyurtmani bekor qilish"""
    bot = Bot(token=BOT_TOKEN)
    order_id = int(callback.data.split("cancel_taken_")[1])
    
    # Buyurtma ma'lumotlarini olish (bekor qilishdan OLDIN)
    order = await get_order(order_id)
    client_id = order['client_id']
    
    # Buyurtmani bekor qilish
    await cancel_order(order_id)
    
    # Haydovchiga xabar
    await callback.message.edit_text(
        f"❌ Buyurtma #{order_id} bekor qilindi\n\n"
        "Buyurtma yana aktiv ro'yxatga qaytarildi."
    )
    
    # Mijozga xabar yuborish
    client_message = (
        f"⚠️ Buyurtma #{order_id} bekor qilindi\n\n"
        f"Haydovchi buyurtmani bekor qildi.\n"
        f"Sizning buyurtmangiz yana aktiv holda qolmoqda.\n"
        f"Boshqa haydovchilar ko'rishadi."
    )
    
    try:
        await bot.send_message(
            chat_id=client_id,
            text=client_message
        )
    except Exception as e:
        print(f"❌ Mijozga bekor qilish xabari yuborishda xatolik: {e}")
    
    await bot.session.close()

# MENING BUYURTMALARIM (haydovchi)
@router.message(F.text == "🚗 Mening buyurtmalarim")
async def my_driver_orders(message: Message):
    """Haydovchi olingan buyurtmalari"""
    orders = await get_driver_active_orders(message.from_user.id)
    
    if not orders:
        await message.answer("❌ Sizda hozir aktiv buyurtmalar yo'q")
        return
    
    await message.answer("🚗 Sizning aktiv buyurtmalaringiz:")
    
    for order in orders:
        direction_text = "🔵 Mangit → Nukus" if order['direction'] == "mangit_nukus" else "🔴 Nukus → Mangit"
        
        order_text = (
            f"🆔 Buyurtma #{order['id']}\n\n"
            f"👤 Mijoz: {order['name']}\n"
            f"📱 Telefon: {order['phone']}\n"
            f"👥 Odam soni: {order['people_count']}\n"
            f"📍 Manzil: {order['address']}\n"
            f"💰 Narx: {order['price'] * order['people_count']:,} so'm\n"
            f"🔄 {direction_text}\n"
            f"📅 {order['created_at'].strftime('%d.%m.%Y %H:%M')}\n\n"
            f"📍 Lokatsiya:\n"
            f"https://www.google.com/maps?q={order['latitude']},{order['longitude']}"
        )
        
        await message.answer(
            order_text,
            reply_markup=get_cancel_order_keyboard(order['id'])
        )
