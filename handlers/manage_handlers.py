from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BotCommand, CallbackQuery
from aiogram.filters import Command, and_f

from config import DB_NAME
from keyboards.general_keyboard import kb_info
from states.staff_states import StaffStates, AdsStates
from utils.database import Database
from utils.my_commands import manage_commands
from keyboards.manage_keyboards import kb_setting, kb_change_info, make_confirm_kb, kb_manage, cancel, cancel_and_back

setting_router = Router()
db = Database(DB_NAME)


# work with Insert new info
@setting_router.message(and_f(F.text == 'Insert new info', StaffStates.admin))
async def setting_handler(message: Message):
    await message.answer(
        text="Choose any info to change:",
        reply_markup=kb_change_info
    )


@setting_router.message(and_f(F.text == 'Modify introduce', StaffStates.admin))
async def modify_introduce_handler(message: Message, state: FSMContext):
    await state.set_state(AdsStates.titleState)
    await message.answer(text='Please, Write a title',reply_markup=cancel)


@setting_router.message(AdsStates.titleState)
async def modify_title_handler(message: Message, state: FSMContext):
    if message.text == "Cancel":
        await message.answer(text="Canceled", reply_markup=kb_change_info)
        await state.set_state(StaffStates.admin)
    elif message.text:
        await state.update_data(title=message.text)
        await state.set_state(AdsStates.infoState)
        await message.answer("Please, write a descriptions",reply_markup=cancel_and_back)
    else:
        await message.answer("Please, write only text")


@setting_router.message(AdsStates.infoState)
async def modify_description_handler(message: Message, state: FSMContext):
    if message.text == "Cancel":
        await message.answer(text="Canceled",reply_markup=kb_change_info)
        await state.set_state(StaffStates.admin)
    elif message.text == "Back":
        await message.answer(text='Please, Write a title', reply_markup=cancel)
        await state.set_state(AdsStates.titleState)
    elif message.text:
        await state.update_data(dis=message.text)
        await state.set_state(AdsStates.imageState)
        await message.answer("Please, send a photo",reply_markup=cancel_and_back)
    else:
        await message.answer("Please, send only text")


@setting_router.message(AdsStates.imageState)
async def modify_description_handler(message: Message, state: FSMContext):
    if message.text == "Cancel":
        await message.answer(text="Canceled",reply_markup=kb_change_info)
        await state.set_state(StaffStates.admin)
    elif message.text == "Back":
        await message.answer("Please, write a descriptions", reply_markup=cancel_and_back)
        await state.set_state(AdsStates.infoState)
    elif message.photo:
        await state.update_data(image=message.photo[-1].file_id)
        all_data = await state.get_data()
        await message.answer_photo(
            photo=all_data.get('image'),
            caption=all_data.get('title') + "\n\n" + all_data.get('dis') + "\n\n Do you want to save?",
            reply_markup=make_confirm_kb()
        )
    else:
        await message.answer("Please, send only photo", reply_markup=cancel_and_back)


@setting_router.callback_query(AdsStates.imageState)
async def callback_query_handler(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'YES':
        all_data = await state.get_data()
        db.update_miran_info(
            title=all_data.get('title'),
            description=all_data.get('dis'),
            image=all_data.get('image')
        )
        await callback.message.delete()
        await callback.message.answer(
            text="Successfully saved!",
            reply_markup=kb_manage
        )
    else:
        await callback.message.delete()
        await callback.message.answer(
            text="All actions cancelled!",
            reply_markup=kb_manage
        )
    await state.set_state(StaffStates.admin)


@setting_router.message(and_f(F.text == 'Back', StaffStates.admin))
async def back_handler(message: Message, state: FSMContext):
    await message.answer(
        text='Manage profile',
        reply_markup=kb_manage
    )
    await state.set_state(StaffStates.admin)


# work with Settings panel
@setting_router.message(and_f(F.text == 'Settings', StaffStates.admin))
async def setting_handler(message: Message, state: FSMContext):
    # await message.bot.set_my_commands(manage_commands)
    await message.answer(
        text="Settings panel",
        reply_markup=kb_setting
    )


@setting_router.message(and_f(F.text == 'Admins list', StaffStates.admin))
async def admins_list_handler(message: Message, state: FSMContext):
    s = ""
    for admin in db.get_admin_list():
        lname = admin[1] if admin[1] is not None else " "
        s += (
            "<b>{} {}</b>\n"
            "\t <i>Contact:</i> {}\n"
            "\t <i>Telegram:</i> {}\n\n"
        ).format(admin[0], lname, admin[2], admin[3])
    await message.answer(text=s)


# work with log out button
@setting_router.message(and_f(F.text == 'Log out', StaffStates.admin))
async def logout_handler(message: Message, state: FSMContext):
    await message.answer(text='Logged out', reply_markup=kb_info)
    await message.bot.set_my_commands(commands=[
        BotCommand(command='start', description='Start/restart bot')
    ])
    await state.clear()
