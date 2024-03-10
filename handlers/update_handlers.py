from aiogram import Router, F
from aiogram.filters import and_f
from aiogram.types import Message, CallbackQuery, BotCommand
from aiogram.fsm.context import FSMContext

from config import DB_NAME
from keyboards.admin_keyboards import kb_admin
from keyboards.general_keyboard import kb_info, back_kb
from keyboards.manage_keyboards import kb_setting, kb_change_info, kb_manage, cancel, cancel_and_back
from utils.database import Database
from states.staff_states import Updates, StaffStates
from keyboards.general_inline_keyboards import done_confirm_kb

update_handler = Router()
db = Database(DB_NAME)


# set updates
@update_handler.message(F.text == 'Insert Updates')
async def insert_updates_handler(message: Message, state: FSMContext):
    await state.set_state(Updates.company)
    await message.answer(
        text='Please, Insert company name: ',
        reply_markup=cancel
    )


@update_handler.message(Updates.company)
async def company_handler(message: Message, state: FSMContext):
    if message.text:
        if message.text == 'Cancel':
            users = db.get_admin_list_all()
            all_data = await state.get_data()

            for user in users:
                if all_data['username'] == user[7] and all_data['password'] == user[8]:
                    if int(user[6]) == 1:
                        await state.set_state(StaffStates.admin)
                        await message.answer(
                            text="Manage profile",
                            reply_markup=kb_manage
                        )
                    else:
                        await state.set_state(StaffStates.user)
                        await message.answer(
                            text="Admins Panel",
                            reply_markup=kb_admin
                        )
        else:
            await state.update_data(company_name=message.text)
            await state.set_state(Updates.truck)
            await message.answer(
                text='Please, Insert truck unit number:',
                reply_markup=cancel_and_back
            )
    else:
        await message.answer("Please, Write only text")


@update_handler.message(Updates.truck)
async def company_handler(message: Message, state: FSMContext):
    if message.text:
        if message.text == 'Cancel':
            users = db.get_admin_list_all()
            all_data = await state.get_data()

            for user in users:
                if all_data['username'] == user[7] and all_data['password'] == user[8]:
                    if int(user[6]) == 1:
                        await state.set_state(StaffStates.admin)
                        await message.answer(
                            text="Manage profile",
                            reply_markup=kb_manage
                        )
                    else:
                        await state.set_state(StaffStates.user)
                        await message.answer(
                            text="Admins Panel",
                            reply_markup=kb_admin
                        )
        elif message.text == 'Back':
            await state.set_state(Updates.company)
            await message.answer(
                text='Please, Insert company name: ',
                reply_markup=cancel
            )
        else:
            await state.update_data(truck_number=message.text)
            await state.set_state(Updates.driver)
            await message.answer(
                text="Please, Write driver's fullname: ",
                reply_markup=cancel_and_back
            )
    else:
        await message.answer("Please, Write only text")


@update_handler.message(Updates.driver)
async def company_handler(message: Message, state: FSMContext):
    if message.text:
        if message.text == 'Cancel':
            users = db.get_admin_list_all()
            all_data = await state.get_data()

            for user in users:
                if all_data['username'] == user[7] and all_data['password'] == user[8]:
                    if int(user[6]) == 1:
                        await state.set_state(StaffStates.admin)
                        await message.answer(
                            text="Manage profile",
                            reply_markup=kb_manage
                        )
                    else:
                        await state.set_state(StaffStates.user)
                        await message.answer(
                            text="Admins Panel",
                            reply_markup=kb_admin
                        )
        elif message.text == 'Back':
            await state.set_state(Updates.truck)
            await message.answer(
                text='Please, Insert truck unit number:',
                reply_markup=cancel_and_back
            )
        else:
            await state.update_data(driver_name=message.text)
            await state.set_state(Updates.issue)
            await message.answer(
                text="Please, Write issue(s): ",
                reply_markup=cancel_and_back
            )
    else:
        await message.answer("Please, Write only text")


@update_handler.message(Updates.issue)
async def company_handler(message: Message, state: FSMContext):
    if message.text:
        if message.text == 'Cancel':
            users = db.get_admin_list_all()
            all_data = await state.get_data()

            for user in users:
                if all_data['username'] == user[7] and all_data['password'] == user[8]:
                    if int(user[6]) == 1:
                        await state.set_state(StaffStates.admin)
                        await message.answer(
                            text="Manage profile",
                            reply_markup=kb_manage
                        )
                    else:
                        await state.set_state(StaffStates.user)
                        await message.answer(
                            text="Admins Panel",
                            reply_markup=kb_admin
                        )
        elif message.text == 'Back':
            await state.set_state(Updates.driver)
            await message.answer(
                text="Please, Write driver's fullname: ",
                reply_markup=cancel_and_back
            )
        else:
            await state.update_data(issue=message.text)
            await state.set_state(Updates.issue)

            all_data = await state.get_data()
            db.set_updates(
                company=all_data.get('company_name'),
                truck=all_data.get('truck_number'),
                driver=all_data.get('driver_name'),
                issue=all_data.get('issue')
            )
            users = db.get_admin_list_all()

            for user in users:
                # print(all_data)
                if all_data['username'] == user[7] and all_data['password'] == user[8]:
                    if int(user[6]) == 1:
                        await state.set_state(StaffStates.admin)
                        await message.answer(
                            text="He/She is successfully posted",
                            reply_markup=kb_manage
                        )
                    else:
                        await state.set_state(StaffStates.user)
                        await message.answer(
                            text="He/She is successfully posted",
                            reply_markup=kb_admin
                        )
            # await state.clear()
    else:
        await message.answer(text="Please, send only text")


@update_handler.message(F.text == 'ELD News')
async def eld_news_handlers(message: Message, state: FSMContext):
    await state.set_state(Updates.eldNewsState)
    await message.answer(
        text="The session has not finished",
        reply_markup=back_kb
    )


@update_handler.message(Updates.eldNewsState)
async def eld_news_handler(message: Message, state: FSMContext):
    users = db.get_admin_list_all()
    all_data = await state.get_data()

    for user in users:
        if all_data['username'] == user[7] and all_data['password'] == user[8]:
            if int(user[6]) == 1:
                await state.set_state(StaffStates.admin)
                await message.answer(
                    text="Manage profile",
                    reply_markup=kb_manage
                )
            else:
                await state.set_state(StaffStates.user)
                await message.answer(
                    text="Admins Panel",
                    reply_markup=kb_admin
                )


# see all updates
@update_handler.message(F.text == 'Updates')
async def get_updates(message: Message, state: FSMContext):
    await state.set_state(Updates.startDoneState)
    updates = db.get_updates()
    for update in updates:
        await message.answer(
            text=f"<b>Company</b>: {update[1]}\n"
                 f"\t   <i>Truck</i>: {update[2]}\n"
                 f"\t   <i>Driver</i>: {update[3]}\n"
                 f"\t   <i>Issue</i>: {update[4]}\n\n",
            reply_markup=done_confirm_kb(update[0]),
        )
    await message.answer(
        text="Done",
        reply_markup=back_kb
    )


@update_handler.callback_query(Updates.startDoneState)
async def done_updates(callback: CallbackQuery, state: FSMContext):
    if db.delete_updates(callback.data):
        await callback.message.delete()
    else:
        await callback.message.answer(
            f"Something went wrong!\n"
            f"Try again later or click /cancel to cancel process"
        )


@update_handler.message(and_f(F.text == "Back", Updates.startDoneState))
async def done_updates(message: Message, state: FSMContext):
    if message.text == 'Back':
        users = db.get_admin_list_all()
        all_data = await state.get_data()

        for user in users:
            if all_data['username'] == user[7] and all_data['password'] == user[8]:
                if int(user[6]) == 1:
                    await state.set_state(StaffStates.admin)
                    await message.answer(
                        text="Manage panel",
                        reply_markup=kb_manage
                    )
                else:
                    await state.set_state(StaffStates.user)
                    await message.answer(
                        text="Admins panel",
                        reply_markup=kb_admin
                    )
