from aiogram import F, Router
from aiogram.filters import and_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BotCommand

from keyboards.general_keyboard import kb_info
from states.staff_states import StaffStates

user_router = Router()


@user_router.message(and_f(F.text == "Log out", StaffStates.user))
async def user_logout_handler(message: Message, state: FSMContext):
    await message.answer(text="Log out", reply_markup=kb_info)
    await message.bot.set_my_commands(commands=[
        BotCommand(command='start', description='Start/restart bot')
    ])
    await state.clear()
