from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_people_count_keyboard():
    """Odam soni klaviaturasi"""
    keyboard = [
        [
            InlineKeyboardButton(text="1️⃣", callback_data="people_1"),
            InlineKeyboardButton(text="2️⃣", callback_data="people_2"),
            InlineKeyboardButton(text="3️⃣", callback_data="people_3"),
            InlineKeyboardButton(text="4️⃣", callback_data="people_4")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_direction_keyboard():
    """Yo'nalish klaviaturasi"""
    keyboard = [
        [InlineKeyboardButton(text="🔵 Mangit → Nukus", callback_data="direction_mangit_nukus")],
        [InlineKeyboardButton(text="🔴 Nukus → Mangit", callback_data="direction_nukus_mangit")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_confirm_keyboard():
    """Tasdiqlash klaviaturasi"""
    keyboard = [
        [InlineKeyboardButton(text="✅ Buyurtma berish", callback_data="confirm_order")],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_order")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_order_action_keyboard(order_id: int):
    """Buyurtma harakatlari"""
    keyboard = [
        [InlineKeyboardButton(text="✅ Buyurtmani olish", callback_data=f"take_order_{order_id}")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_cancel_order_keyboard(order_id: int):
    """Buyurtmani bekor qilish"""
    keyboard = [
        [InlineKeyboardButton(text="❌ Buyurtmani bekor qilish", callback_data=f"cancel_taken_{order_id}")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_direction_filter_keyboard():
    """Haydovchi uchun yo'nalish tanlash"""
    keyboard = [
        [InlineKeyboardButton(text="🔵 Mangit → Nukus", callback_data="filter_mangit_nukus")],
        [InlineKeyboardButton(text="🔴 Nukus → Mangit", callback_data="filter_nukus_mangit")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)