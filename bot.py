import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Получаем токен из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set in environment variables")

# Хранилище штампов (пока в RAM)
user_data = {}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def main_keyboard():
    kb = [
        [InlineKeyboardButton(text="Мои штампы ☕️", callback_data="stamps")],
        [InlineKeyboardButton(text="Добавить штамп ➕", callback_data="add")],
        [InlineKeyboardButton(text="Использовать бесплатный кофе 🎉", callback_data="use")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


@dp.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_data:
        user_data[user_id] = 0

    welcome_text = (
        "☕️ *Добро пожаловать в MollyCaffee!* \n\n"
        "Мы рады видеть вас в нашей программе лояльности.\n\n"
        "Как это работает:\n"
        "• За каждый купленный кофе вы получаете *1 штамп*.\n"
        "• Когда вы собираете *10 штампов*, вы получаете *бесплатный кофе* 🎉\n"
        "• Следить за прогрессом, добавлять штампы и активировать бесплатный кофе можно прямо в этом боте.\n\n"
        "Ниже — меню управления вашими штампами ⬇️"
    )

    # используем Markdown-style (aiogram auto форматирования)
    await message.answer(welcome_text, reply_markup=main_keyboard())


@dp.callback_query(F.data == "stamps")
async def show_stamps(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    stamps = user_data.get(user_id, 0)

    bar = "".join(["🟤" if i < stamps else "⚪️" for i in range(10)])

    if stamps < 10:
        text = (
            f"Ваши штампы: {stamps}/10\n\n"
            f"{bar}\n\n"
            f"Ещё {10 - stamps} шт. до бесплатного кофе! ☕️"
        )
    else:
        text = (
            "🎉 У вас уже 10 штампов!\n"
            "Вы можете получить бесплатный кофе."
        )

    # edit_text безопасно, но сначала проверим есть ли сообщение
    try:
        await callback.message.edit_text(text, reply_markup=main_keyboard())
    except Exception:
        await callback.message.answer(text, reply_markup=main_keyboard())
    await callback.answer()


@dp.callback_query(F.data == "add")
async def add_stamp(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    stamps = user_data.get(user_id, 0)

    if stamps >= 10:
        await callback.answer("У вас уже есть бесплатный кофе 🎉", show_alert=True)
        return

    user_data[user_id] = stamps + 1
    await callback.answer("Штамп добавлен! ☕️")
    await show_stamps(callback)


@dp.callback_query(F.data == "use")
async def use_free_coffee(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    stamps = user_data.get(user_id, 0)

    if stamps < 10:
        await callback.answer("У вас нет бесплатного кофе 👀", show_alert=True)
        return

    user_data[user_id] = 0
    await callback.answer("Бесплатный кофе использован 🎉")
    await show_stamps(callback)


async def main():
    print("Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
