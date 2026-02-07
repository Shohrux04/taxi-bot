from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.reply import get_phone_keyboard, get_main_menu_client, get_main_menu_driver
from states.driver import DriverStates
from services.user_service import create_user, create_driver

router = Router()

# MIJOZ REGISTRATSIYASI
@router.message(F.text == "👤 Mijoz")
async def register_client_name(message: Message, state: FSMContext):
    """Mijoz - ism so'rash"""
    await state.update_data(role='client')
    await message.answer(
        "📝 Ismingizni kiriting:",
        reply_markup=get_phone_keyboard()
    )
    await state.set_state(DriverStates.name)

# HAYDOVCHI REGISTRATSIYASI
@router.message(F.text == "🚗 Haydovchi")
async def register_driver_name(message: Message, state: FSMContext):
    """Haydovchi - ism so'rash"""
    await state.update_data(role='driver')
    await message.answer(
        "📝 Ismingizni kiriting:",
        reply_markup=get_phone_keyboard()
    )
    await state.set_state(DriverStates.name)

# ISM QABUL QILISH
@router.message(DriverStates.name)
async def process_name(message: Message, state: FSMContext):
    """Ism qabul qilish"""
    await state.update_data(name=message.text)
    await message.answer(
        "📱 Telefon raqamingizni yuboring:",
        reply_markup=get_phone_keyboard()
    )
    await state.set_state(DriverStates.phone)

# TELEFON QABUL QILISH
@router.message(DriverStates.phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    """Telefon (contact) qabul qilish"""
    data = await state.get_data()
    phone = message.contact.phone_number
    
    if data['role'] == 'client':
        # Mijozni saqlash
        await create_user(
            user_id=message.from_user.id,
            role='client',
            name=data['name'],
            phone=phone
        )
        await message.answer(
            "✅ Muvaffaqiyatli ro'yxatdan o'tdingiz!",
            reply_markup=get_main_menu_client()
        )
        await state.clear()
    else:
        # Haydovchi uchun mashina ma'lumotlari
        await state.update_data(phone=phone)
        await message.answer(
            "🚗 Mashina rusumini kiriting:\n\n"
            "Masalan: Cobalt, Nexia, Damas"
        )
        await state.set_state(DriverStates.car_model)

@router.message(DriverStates.phone)
async def process_phone_text(message: Message, state: FSMContext):
    """Telefon (matn) qabul qilish"""
    data = await state.get_data()
    phone = message.text
    
    if data['role'] == 'client':
        # Mijozni saqlash
        await create_user(
            user_id=message.from_user.id,
            role='client',
            name=data['name'],
            phone=phone
        )
        await message.answer(
            "✅ Muvaffaqiyatli ro'yxatdan o'tdingiz!",
            reply_markup=get_main_menu_client()
        )
        await state.clear()
    else:
        # Haydovchi uchun mashina ma'lumotlari
        await state.update_data(phone=phone)
        await message.answer(
            "🚗 Mashina rusumini kiriting:\n\n"
            "Masalan: Cobalt, Nexia, Damas"
        )
        await state.set_state(DriverStates.car_model)

# MASHINA RUSUMI
@router.message(DriverStates.car_model)
async def process_car_model(message: Message, state: FSMContext):
    """Mashina rusumini qabul qilish"""
    await state.update_data(car_model=message.text)
    await message.answer(
        "🔢 Mashina raqamini kiriting:\n\n"
        "Masalan: 01 A 123 BC"
    )
    await state.set_state(DriverStates.car_number)

# MASHINA RAQAMI
@router.message(DriverStates.car_number)
async def process_car_number(message: Message, state: FSMContext):
    """Mashina raqamini qabul qilish va saqlash"""
    data = await state.get_data()
    
    # Haydovchini saqlash
    await create_user(
        user_id=message.from_user.id,
        role='driver',
        name=data['name'],
        phone=data['phone']
    )
    
    await create_driver(
        user_id=message.from_user.id,
        car_model=data['car_model'],
        car_number=message.text
    )
    
    await message.answer(
        "✅ Muvaffaqiyatli ro'yxatdan o'tdingiz!",
        reply_markup=get_main_menu_driver()
    )
    await state.clear()