from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove


message_router = Router()


@message_router.message(F.text == 'Contact')
async def contact_handler(message: Message):
    await message.answer(
         text=f"<b>Contacts</b>:\n"
              f"\t  <b>CEO</b>: Suhrob Khakimov  (+998 93 551 51 96)\n"
              f"\t  <b>Manager</b>: Muzrob Nasirov (+998 93 448 26 22)\n"
              f"\t  <b>Supervisor</b>: Islom Isamiddinov (+998 93 073 51 23)\n"
              f"\t  <b>Supervisor</b>: Begzod Nasirov (+998 93 073 51 23)",
        reply_markup=ReplyKeyboardRemove()
    )
