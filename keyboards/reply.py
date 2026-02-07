from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_role_keyboard():
    """Rol tanlash klaviaturasi"""
    keyboard = [
        [KeyboardButton(text="👤 Mijoz"), KeyboardButton(text="🚗 Haydovchi")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_phone_keyboard():
    """Telefon yuborish klaviaturasi"""
    keyboard = [
        [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_location_keyboard():
    """Lokatsiya yuborish klaviaturasi"""
    keyboard = [
        [KeyboardButton(text="📍 Lokatsiyani yuborish", request_location=True)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_main_menu_client():
    """Mijoz asosiy menyu"""
    keyboard = [
        [KeyboardButton(text="🚕 Buyurtma berish")],
        [KeyboardButton(text="📋 Mening buyurtmalarim")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_main_menu_driver():
    """Haydovchi asosiy menyu"""
    keyboard = [
        [KeyboardButton(text="📋 Buyurtmalar ro'yxati")],
        [KeyboardButton(text="🚗 Mening buyurtmalarim")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)