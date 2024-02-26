from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

from config import DB_NAME
from utils.database import Database
from keyboards.general_keyboard import kb_info

cmd_router = Router()
db = Database(DB_NAME)


@cmd_router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    info = db.get_miran_info()
    await message.answer_photo(
        photo=info[1],
        caption=info[0] + "\n\n" + info[2],
        reply_markup=kb_info
    )
    await state.clear()
