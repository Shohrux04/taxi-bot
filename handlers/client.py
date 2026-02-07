from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline import (
    get_people_count_keyboard, 
    get_direction_keyboard, 
    get_confirm_keyboard
)
from keyboards.reply import get_location_keyboard, get_main_menu_client
from states.client import ClientStates
from services.order_service import create_order, get_user_orders

router = Router()

# BUYURTMA BERISH BOSHLASH
@router.message(F.text == "🚕 Buyurtma berish")
async def start_order(message: Message, state: FSMContext):
    """Buyurtma berish jarayonini boshlash"""
    await message.answer(
        "👥 Necha kishi yo'lga chiqasiz?",
        reply_markup=get_people_count_keyboard()
    )
    await state.set_state(ClientStates.people_count)

# ODAM SONI
@router.callback_query(ClientStates.people_count, F.data.startswith("people_"))
async def process_people_count(callback: CallbackQuery, state: FSMContext):
    """Odam sonini qabul qilish"""
    count = int(callback.data.split("_")[1])
    await state.update_data(people_count=count)
    
    await callback.message.edit_text(f"✅ Odam soni: {count}")
    await callback.message.answer(
        "📍 Manzilni kiriting:\n\n"
        "Masalan: Mangit, Madaniyat ko'chasi 12-uy"
    )
    await state.set_state(ClientStates.address)

# MANZIL
@router.message(ClientStates.address)
async def process_address(message: Message, state: FSMContext):
    """Manzilni qabul qilish"""
    await state.update_data(address=message.text)
    await message.answer(
        "💰 1 kishi uchun taklif summangizni kiriting (so'm):\n\n"
        "Masalan: 50000"
    )
    await state.set_state(ClientStates.price)

# NARX
@router.message(ClientStates.price)
async def process_price(message: Message, state: FSMContext):
    """Narxni qabul qilish"""
    try:
        price = int(message.text)
        await state.update_data(price=price)
        await message.answer(
            "🔄 Yo'nalishni tanlang:",
            reply_markup=get_direction_keyboard()
        )
        await state.set_state(ClientStates.direction)
    except ValueError:
        await message.answer("❌ Iltimos, faqat raqam kiriting!")

# YO'NALISH
@router.callback_query(ClientStates.direction, F.data.startswith("direction_"))
async def process_direction(callback: CallbackQuery, state: FSMContext):
    """Yo'nalishni qabul qilish"""
    direction = callback.data.split("direction_")[1]
    await state.update_data(direction=direction)
    
    direction_text = "🔵 Mangit → Nukus" if direction == "mangit_nukus" else "🔴 Nukus → Mangit"
    await callback.message.edit_text(f"✅ Yo'nalish: {direction_text}")
    
    await callback.message.answer(
        "📍 Lokatsiyangizni yuboring:",
        reply_markup=get_location_keyboard()
    )
    await state.set_state(ClientStates.location)

# LOKATSIYA
@router.message(ClientStates.location, F.location)
async def process_location(message: Message, state: FSMContext):
    """Lokatsiyani qabul qilish"""
    await state.update_data(
        latitude=message.location.latitude,
        longitude=message.location.longitude
    )
    
    # Ma'lumotlarni ko'rsatish
    data = await state.get_data()
    direction_text = "🔵 Mangit → Nukus" if data['direction'] == "mangit_nukus" else "🔴 Nukus → Mangit"
    
    summary = (
        "📋 Buyurtma ma'lumotlari:\n\n"
        f"👥 Odam soni: {data['people_count']}\n"
        f"📍 Manzil: {data['address']}\n"
        f"💰 Narx (1 kishi): {data['price']:,} so'm\n"
        f"🔄 Yo'nalish: {direction_text}\n"
        f"📍 Lokatsiya: {data['latitude']:.6f}, {data['longitude']:.6f}\n\n"
        f"💵 Jami: {data['price'] * data['people_count']:,} so'm"
    )
    
    await message.answer(
        summary,
        reply_markup=get_confirm_keyboard()
    )
    await state.set_state(ClientStates.confirm)

# TASDIQLASH
@router.callback_query(ClientStates.confirm, F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    """Buyurtmani tasdiqlash va saqlash"""
    data = await state.get_data()
    
    # Buyurtmani saqlash
    order_id = await create_order(
        client_id=callback.from_user.id,
        people_count=data['people_count'],
        address=data['address'],
        price=data['price'],
        direction=data['direction'],
        latitude=data['latitude'],
        longitude=data['longitude']
    )
    
    await callback.message.edit_text(
        f"✅ Buyurtma #{order_id} muvaffaqiyatli yaratildi!\n\n"
        "Haydovchilar tez orada bog'lanishadi."
    )
    await callback.message.answer(
        "Bosh menyu:",
        reply_markup=get_main_menu_client()
    )
    await state.clear()

# BEKOR QILISH
@router.callback_query(ClientStates.confirm, F.data == "cancel_order")
async def cancel_order_creation(callback: CallbackQuery, state: FSMContext):
    """Buyurtma yaratishni bekor qilish"""
    await callback.message.edit_text("❌ Buyurtma bekor qilindi")
    await callback.message.answer(
        "Bosh menyu:",
        reply_markup=get_main_menu_client()
    )
    await state.clear()

# MENING BUYURTMALARIM
@router.message(F.text == "📋 Mening buyurtmalarim")
async def my_orders(message: Message):
    """Foydalanuvchi buyurtmalarini ko'rsatish"""
    orders = await get_user_orders(message.from_user.id)
    
    if not orders:
        await message.answer("❌ Sizda hali buyurtmalar yo'q")
        return
    
    response = "📋 Sizning buyurtmalaringiz:\n\n"
    
    for order in orders:
        direction_text = "🔵 Mangit → Nukus" if order['direction'] == "mangit_nukus" else "🔴 Nukus → Mangit"
        status_text = {
            'active': '🟡 Aktiv',
            'taken': '🟢 Qabul qilindi',
            'cancelled': '🔴 Bekor qilindi'
        }.get(order['status'], order['status'])
        
        response += (
            f"🆔 #{order['id']}\n"
            f"👥 {order['people_count']} kishi\n"
            f"📍 {order['address']}\n"
            f"💰 {order['price']:,} so'm\n"
            f"🔄 {direction_text}\n"
            f"📊 {status_text}\n"
            f"📅 {order['created_at'].strftime('%d.%m.%Y %H:%M')}\n"
            "─────────────\n\n"
        )
    
    await message.answer(response)