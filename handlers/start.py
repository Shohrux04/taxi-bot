from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.reply import get_role_keyboard, get_main_menu_client, get_main_menu_driver
from services.user_service import get_user

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Start buyrug'i"""
    await state.clear()
    
    user = await get_user(message.from_user.id)
    
    if user:
        # Foydalanuvchi mavjud
        if user['role'] == 'client':
            await message.answer(
                f"Assalomu aleykum, {user['name']}!\n\n"
                "Siz mijoz sifatida ro'yxatdan o'tgansiz.",
                reply_markup=get_main_menu_client()
            )
        else:
            await message.answer(
                f"Assalomu aleykum, {user['name']}!\n\n"
                "Siz haydovchi sifatida ro'yxatdan o'tgansiz.",
                reply_markup=get_main_menu_driver()
            )
    else:
        # Yangi foydalanuvchi
        await message.answer(
            "👋 Assalomu aleykum!\n\n"
            "🚕 Mangit-Nukus Taxi botiga xush kelibsiz!\n\n"
            "Iltimos, rolni tanlang:",
            reply_markup=get_role_keyboard()
        )