from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import DB_NAME
from utils.database import Database
from states.staff_states import Updates
from keyboards.general_inline_keyboards import done_confirm_kb

update_handler = Router()
db = Database(DB_NAME)


# set updates
@update_handler.message(F.text == 'Insert Updates')
async def insert_updates_handler(message: Message, state: FSMContext):
    await state.set_state(Updates.company)
    await message.answer(
        text='Please, Insert company name: '
    )


@update_handler.message(Updates.company)
async def company_handler(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(company_name=message.text)
        await state.set_state(Updates.truck)
        await message.answer(
            text='Please, Insert truck name: '
        )
    else:
        await message.answer("Please, Write only text")


@update_handler.message(Updates.truck)
async def company_handler(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(truck_number=message.text)
        await state.set_state(Updates.driver)
        await message.answer(
            text="Please, Write driver's fullname: "
        )
    else:
        await message.answer("Please, Write only text")


@update_handler.message(Updates.driver)
async def company_handler(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(driver_name=message.text)
        await state.set_state(Updates.issue)
        await message.answer(
            text="Please, Write issue(s): "
        )
    else:
        await message.answer("Please, Write only text")


@update_handler.message(Updates.issue)
async def company_handler(message: Message, state: FSMContext):
    await state.update_data(issue=message.text)
    await state.set_state(Updates.issue)

    all_data = await state.get_data()
    db.set_updates(
        company=all_data.get('company_name'),
        truck=all_data.get('truck_number'),
        driver=all_data.get('driver_name'),
        issue=all_data.get('issue')
    )

    await message.answer(
        text="He/She is successfully posted"
    )
    await state.clear()


# see all updates
@update_handler.message(F.text == 'Updates')
async def get_updates(message: Message, state: FSMContext):
    await state.set_state(Updates.startDoneState)
    updates = db.get_updates()
    for update in updates:
        u_id = update[0]
        await message.answer(
            text=f"<b>Company</b>: {update[1]}\n"
                 f"\t   <i>Truck</i>: {update[2]}\n"
                 f"\t   <i>Driver</i>: {update[3]}\n"
                 f"\t   <i>Issue</i>: {update[4]}\n\n",
            reply_markup=done_confirm_kb(update[0])
        )


@update_handler.callback_query(Updates.startDoneState)
async def done_updates(callback: CallbackQuery, state: FSMContext):
    if db.delete_updates(callback.data):
        await callback.message.delete()
        await state.clear()
    else:
        await callback.message.answer(
            f"Something went wrong!\n"
            f"Try again later or click /cancel to cancel process"
        )
