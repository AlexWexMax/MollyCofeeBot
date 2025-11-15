from aiogram import types
from config import BARISTA_PASSWORD
from db import add_stamp, use_qr, get_stamps

BARISTA_SESSIONS = set()  # хранит user_id авторизованных бариста

async def authorize_barista(message: types.Message, password: str):
    if password == BARISTA_PASSWORD:
        BARISTA_SESSIONS.add(message.from_user.id)
        await message.answer("✅ Вы авторизованы как бариста")
    else:
        await message.answer("❌ Неверный пароль")

def is_authorized(user_id: int) -> bool:
    return user_id in BARISTA_SESSIONS

async def process_qr(message: types.Message, qr_id: str):
    if not is_authorized(message.from_user.id):
        await message.answer("❌ Вы не авторизованы")
        return

    user_id = use_qr(qr_id)
    if not user_id:
        await message.answer("❌ QR-код недействителен или уже использован")
        return

    add_stamp(user_id)
    stamps = get_stamps(user_id)
    await message.answer(f"✅ Штамп добавлен пользователю {user_id}. Теперь {stamps} штампов.")
