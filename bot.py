import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from config import BOT_TOKEN
from db import init_db, add_user
from client import main_keyboard, show_stamps
from qr_utils import generate_qr
from barista import authorize_barista, process_qr, is_authorized

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Инициализация базы
init_db()

@dp.message(Command("start"))
async def start(message: types.Message):
    add_user(message.from_user.id)
    welcome_text = (
        "☕️ *Добро пожаловать в MollyCaffee!* \n\n"
        "Мы рады видеть вас в нашей программе лояльности.\n\n"
        "Ниже — меню управления вашими штампами ⬇️"
    )
    await message.answer(welcome_text, reply_markup=main_keyboard())

@dp.callback_query(F.data == "stamps")
async def callback_show_stamps(callback: types.CallbackQuery):
    await show_stamps(callback)

@dp.callback_query(F.data == "add")
async def callback_add_stamp(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    qr_id, path = generate_qr(user_id)
    from db import create_qr
    create_qr(qr_id, user_id)
    await callback.message.answer_photo(photo=open(path, "rb"), caption="Покажите этот QR баристе для добавления штампа")
    await callback.answer()

@dp.callback_query(F.data == "use")
async def callback_use_coffee(callback: types.CallbackQuery):
    from db import get_stamps, reset_stamps
    stamps = get_stamps(callback.from_user.id)
    if stamps < 10:
        await callback.answer("У вас нет бесплатного кофе 👀", show_alert=True)
        return
    reset_stamps(callback.from_user.id)
    await callback.answer("Бесплатный кофе использован 🎉")
    await show_stamps(callback)

# Бариста команды
@dp.message(F.text.startswith("/auth"))
async def cmd_auth(message: types.Message):
    password = message.text.split(" ", 1)[-1]
    await authorize_barista(message, password)

@dp.message(F.text.startswith("/qr"))
async def cmd_qr(message: types.Message):
    qr_id = message.text.split(" ", 1)[-1]
    await process_qr(message, qr_id)

async def main():
    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
