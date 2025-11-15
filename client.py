from aiogram import types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from db import get_stamps, create_qr
from qr_utils import generate_qr

def main_keyboard():
    kb = [
        [InlineKeyboardButton(text="Мои штампы ☕️", callback_data="stamps")],
        [InlineKeyboardButton(text="Добавить штамп ➕", callback_data="add")],
        [InlineKeyboardButton(text="Использовать бесплатный кофе 🎉", callback_data="use")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

async def show_stamps(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    stamps = get_stamps(user_id)
    bar = "".join(["🟤" if i < stamps else "⚪️" for i in range(10)])
    if stamps < 10:
        text = f"Ваши штампы: {stamps}/10\n\n{bar}\n\nЕщё {10 - stamps} шт. до бесплатного кофе! ☕️"
    else:
        text = "🎉 У вас уже 10 штампов!\nВы можете получить бесплатный кофе."
    await callback.message.edit_text(text, reply_markup=main_keyboard())
    await callback.answer()
