from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.general_keyboard import kb_info
from utils.database import Database
from config import BOT_TOKEN, DB_NAME
from keyboards.admin_keyboards import kb_admin
from keyboards.manage_keyboards import kb_manage
from states.staff_states import StaffStates

message_router = Router()
bot = Bot(BOT_TOKEN)
dp = Dispatcher()
db = Database(DB_NAME)


@message_router.message(F.text == 'Contact')
async def contact_handler(message: Message):
    await message.answer(
         text=f"Contacts:\n"
              f"\t  CEO: Suhrob Khakimov\n"
              f"\t            `+998 93 551 51 96`\n"
              f"\t  Manager: Muzrob Nasirov\n"
              f"\t            `+998 93 448 26 22`\n"
              f"\t  Supervisor: Islom Formanov\n"
              f"\t            `+998 93 073 51 23`\n"
              f"\t  Supervisor: Begzod Juraev\n"
              f"\t            `+998 99 491 23 08`\n",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=kb_info
    )


@message_router.message(F.text == 'Location')
async def location_handler(message: Message):
    latitude = 41.298212
    longitude = 69.212907

    await bot.send_location(message.chat.id, float(latitude), longitude)
    await message.reply(
        text="Location sent!",
        reply_markup=kb_info
    )


@message_router.message(F.text == 'Miran Team Info')
async def miran_info_desc_handler(message: Message):
    miran_info_desc = db.get_miran_info_desc()

    await message.answer_video(
        video=miran_info_desc[0],
        caption=miran_info_desc[1],
        reply_markup=kb_info
    )


@message_router.message(F.text == 'Services')
async def miran_services_handler(message: Message):
    s = "Miran Team Logistics Services\n\n"
    s += f"\t -Dispatcher\n"
    s += f"\t -ELD Services\n"
    s += f"\t -Company Fleet Services\n"
    s += f"\t -Recruiting Services\n\n"
    s += f"\t -Miran Team Logistics School\n\n"
    s += f"Contact: `+998 93 551 51 96`"

    await message.answer(
        text=s, reply_markup=kb_info, parse_mode=ParseMode.MARKDOWN
    )


@message_router.message(F.text == 'Login')
async def check_handler(message: Message, state: FSMContext):
    await state.set_state(StaffStates.username)
    await message.answer("Please, insert your username: ")


@message_router.message(StaffStates.username)
async def username_handler(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(username=message.text)
        await state.set_state(StaffStates.password)
        await message.answer(
            text="Please, insert your password: "
        )
    else:
        await message.answer("Username consist of text and number\n\nPlease, send again!")


@message_router.message(StaffStates.password)
async def password_handler(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(password=message.text)
        await state.set_state(StaffStates.password)

        all_data = await state.get_data()
        user = db.get_user(username=all_data.get('username'), password=all_data.get('password'))

        if not user:
            await message.answer(
                text=f"There is no such user\n\n"
                     f"Please, contact with your manager to get username\n\n"
                     f"<b>Contact</b>: <a href='https://t.me/logbook_department'>Manager</a>",
                disable_web_page_preview=True,
                reply_markup=kb_info
            )
            await state.set_state(StaffStates.user)
        else:
            if user[3]:
                # await state.update_data(manage_handler='manage')
                await state.set_state(StaffStates.admin)
                await message.answer(
                    text=f'Manage profile',
                    reply_markup=kb_manage
                )
            else:
                # await state.update_data(admin_handler='admin')
                await state.set_state(StaffStates.user)
                await message.answer(
                    text=f'Admin profile',
                    reply_markup=kb_admin
                )
    else:
        await message.answer("Password consist of text and number\n\nPlease, send again!")
    # await state.clear()
