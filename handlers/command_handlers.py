from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

from Miran_ELD_Team.keyboards.info_keyboard import kb_info

cmd_router = Router()


@cmd_router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        f"Assalomu alaykum <b>{message.from_user.first_name}</b>\n\n"
                         f"Welcome to <b>Miran Team ELD</b>",
        reply_markup=kb_info
    )
