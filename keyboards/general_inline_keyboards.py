from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import DB_NAME
from utils.database import Database

db = Database(DB_NAME)


def done_confirm_kb(update_id):
    # print(updates_id)
    rows = [
        InlineKeyboardButton(text=f'✅ ID: {update_id}', callback_data=str(update_id))
    ]
    inl_kb = InlineKeyboardMarkup(
        inline_keyboard=[rows]
    )
    return inl_kb
