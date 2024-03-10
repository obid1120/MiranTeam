from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BotCommand, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, and_f

from config import DB_NAME
from keyboards.general_keyboard import kb_info, back_kb
from states.staff_states import StaffStates, AdsStates, AdminsStates
from utils.database import Database
from utils.my_commands import manage_commands
from keyboards.manage_keyboards import kb_setting, kb_change_info, make_confirm_kb, kb_manage, cancel, cancel_and_back, \
    admin_list_kb, modify_kb, cancel_skip_kb, skip_back_cancel_kb

setting_router = Router()
db = Database(DB_NAME)


# work with Insert new info
@setting_router.message(and_f(F.text == 'Insert new info', StaffStates.admin))
async def setting_handler(message: Message):
    await message.answer(
        text="Choose any info to change:",
        reply_markup=kb_change_info
    )


# work with editing introduce
@setting_router.message(and_f(F.text == 'Edit introduce', StaffStates.admin))
async def modify_introduce_handler(message: Message, state: FSMContext):
    await state.set_state(AdsStates.titleState)
    await message.answer(text='Please, Write a title', reply_markup=cancel)


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


# work with editing miran info
@setting_router.message(and_f(F.text == 'Edit miran info', StaffStates.admin))
async def miran_info_edit_handler(message: Message, state: FSMContext):
    await state.set_state(AdsStates.miranInfoVideoState)
    await message.answer(text="Please, send video...")


@setting_router.message(and_f(AdsStates.miranInfoVideoState))
async def miran_video_handler(message: Message, state: FSMContext):
    if message.video:
        await state.update_data(video=message.video.file_id)
        await state.set_state(AdsStates.miranInfoDescState)
        await message.answer(text="Please, write Miran Info Description...")
    else:
        await message.answer(text="Please, send only video format")


@setting_router.message(and_f(AdsStates.miranInfoDescState))
async def miran_desc_handler(message: Message, state: FSMContext):
    if message.text:
        await state.update_data(description=message.text)
        await state.set_state(AdsStates.miranInfoSaveState)
        await message.answer(
            text="Do you want to save?",
            reply_markup=make_confirm_kb()
        )
    else:
        await message.answer(text="Please, send only text type message")


@setting_router.callback_query(AdsStates.miranInfoSaveState)
async def miran_info_save_handler(query: CallbackQuery, state: FSMContext):
    if query.data == 'YES':
        all_data = await state.get_data()
        video = all_data['video']
        description = all_data['description']
        db.set_miran_info_desc(
            video=video,
            description=description
        )
        await query.message.delete()
        await query.message.answer(
            text="Successfully saved",
            reply_markup=kb_manage
        )
    else:
        await query.message.delete()
        await query.message.answer(
            text="All actions cancelled!",
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
    admins = db.get_admin_list_all()
    await state.set_state(AdminsStates.adminState)

    if admins:
        admin_count = len(admins)
        page_count = int(admin_count/5)+1 if admin_count % 5 != 0 else int(admin_count/5)
        admins_packages = []

        for i in range(0, admin_count, 5):
            admin_package_slice = []
            for j in range(i, i+5):
                try:
                    admin_package_slice.append(admins[j])
                except IndexError:
                    break
            admins_packages.append(admin_package_slice)
        first_admin_list = len(admins_packages[0])

        s = ""
        if admin_count < 5:
            await state.update_data(index=0)
            await state.update_data(admin_list=admin_count)
            await state.update_data(page_count=page_count)
            await state.update_data(admins_packages=admins_packages)
            for i in range(admin_count):
                f_name = admins[i][2] if admins[i][2] is not None else ""
                s += f"<b>{i+1}.</b> {admins[i][1]} {f_name}\n"
            kb = admin_list_kb(all_count=admin_count, count=admin_count)
            await message.answer(
                text=s, reply_markup=kb
            )
        else: 
            await state.update_data(index=0)
            await state.update_data(admin_list=admin_count)
            await state.update_data(page_count=page_count)
            await state.update_data(admins_packages=admins_packages)

            for i in range(5):
                l_name = admins[i][2] if admins[i][2] else ""
                s += f"<b>{i+1}.</b> {admins[i][1]} {l_name}\t  ||\t  {admins[i][3]}\n"
            kb = admin_list_kb(all_count=admin_count, count=first_admin_list)
            await message.answer(
                text=f"<b>Result:</b>\t {1}/{page_count}\n\n{s}",
                reply_markup=kb,
                parse_mode="HTML"
            )
            await message.answer(
                text="Done",
                reply_markup=back_kb
            )


@setting_router.message(and_f(F.text == 'Back', AdminsStates.adminState))
async def back_handler(message: Message, state: FSMContext):
    await state.set_state(StaffStates.admin)
    await message.answer(
        text=f'Manage profile',
        reply_markup=kb_manage
    )


@setting_router.callback_query(AdminsStates.adminState)
async def callback_handler(query: CallbackQuery, state: FSMContext):
    if query.data == 'prev' or query.data == 'next':
        all_data = await state.get_data()
        page_index = all_data.get('index')
        count = all_data.get('admin_list')
        page_count = all_data.get('page_count')
        admins_packages = all_data.get('admins_packages')

        if query.data == 'next':
            if page_index == page_count - 1:
                page_index = 0
            else:
                page_index += 1
        else:
            if page_index == 0:
                page_index = page_count - 1
            else:
                page_index -= 1

        s = ""
        for i in range(len(admins_packages[page_index])):
            l_name = admins_packages[page_index][i][2] if admins_packages[page_index][i][2] else ""
            s += f"<b>{i + 1}</b>. {admins_packages[page_index][i][1]} {l_name}\t  ||\t  {admins_packages[page_index][i][3]}\n"
        await state.update_data(index=page_index)
        kb = admin_list_kb(all_count=count, count=len(admins_packages[page_index]))
        await query.message.edit_text(
            text=f"<b>Result:</b>\t {page_index + 1}/{page_count}\n\n{s}",
            reply_markup=kb,
            parse_mode="HTML"
        )
    elif query.data == "delete" or query.data == "edit":
        if query.data == "edit":
            all_data = await state.get_data()
            admin_id = all_data['admin_id']
            admin_fname = all_data.get('admin_fname')
            admin_lname = all_data.get('admin_lname')
            lname = admin_lname if admin_lname else ""
            s = f"<i>{admin_fname} {lname}</i>\n\n"
            await state.set_state(AdminsStates.editAdminState)
            await state.update_data(admin_id=admin_id)
            await query.message.delete()
            await query.message.answer(
                text=f"{s}Please, enter new firstname...",
                reply_markup=cancel
            )
        else:
            all_data = await state.get_data()
            admin_id = all_data.get('admin_id')
            admin_fname = all_data.get('admin_fname')
            admin_lname = all_data.get('admin_lname')
            lname = admin_lname if admin_lname else ""
            s = f"<b>ID:</b> {admin_id}\n<i>{admin_fname} {lname}</i>\n\n"
            await state.set_state(AdminsStates.removeAdminState)
            await query.message.edit_text(
                text=f"{s}Are you sure to delete?",
                reply_markup=make_confirm_kb()
            )
    else:
        all_data = await state.get_data()
        page_index = all_data['index']
        admins_packages = all_data['admins_packages']

        l_name = admins_packages[page_index][int(query.data)][2] if admins_packages[page_index][int(query.data)][2] else " "
        s = (
            f"{admins_packages[page_index][int(query.data)][1]} "
            f"{l_name}\t  || \t  {admins_packages[page_index][int(query.data)][3]}\n\n"
            f"Contact: `{admins_packages[page_index][int(query.data)][4]}`\n"
            f"Telegram: `{admins_packages[page_index][int(query.data)][5]}`\n"
            f"ID: {admins_packages[page_index][int(query.data)][0]}\n"
        )
        await state.update_data(admin_id=admins_packages[page_index][int(query.data)][0])
        await state.update_data(admin_fname=admins_packages[page_index][int(query.data)][1])
        await state.update_data(admin_lname=admins_packages[page_index][int(query.data)][2])

        await query.message.delete()
        await query.message.answer(
            text=s,
            reply_markup=modify_kb,
            parse_mode=ParseMode.MARKDOWN
        )


@setting_router.callback_query(AdminsStates.removeAdminState)
async def remove_admin_handler(query: CallbackQuery, state: FSMContext):
    if query.data == "YES":
        all_data = await state.get_data()
        admin_id = all_data['admin_id']
        db.remove_admin(
            admin_id=admin_id
        )
        await query.message.delete()
        await query.message.answer(
            text=f"<b>ID:</b> {admin_id}\n\nSuccessfully deleted",
            reply_markup=kb_manage
        )

    if query.data == "NO":
        await state.set_state(StaffStates.admin)
        await query.message.delete()
        await query.message.answer(
            text='Canceled', reply_markup=kb_manage
        )
    await state.set_state(StaffStates.admin)


# add admin
@setting_router.message(and_f(F.text == 'Add admin', AdminsStates.adminState))
async def add_admin_handler(message: Message, state: FSMContext):

    await state.set_state(AdminsStates.editAdminState)
    await state.update_data(add_admin='add_admin')
    await message.answer(
        text=f"Please, enter new firstname...",
        reply_markup=cancel
    )


# edit admin profile
@setting_router.message(and_f(AdminsStates.editAdminState))
async def modify_firstname_handler(message: Message, state: FSMContext):
    if message.text:
        if message.text == "Cancel":
            await state.set_state(StaffStates.admin)
            await message.answer(
                text='Canceled', reply_markup=kb_manage
            )
        else:
            await state.update_data(first_name=message.text)
            await state.set_state(AdminsStates.adminFirstnameState)
            await message.answer(
                text="Please, text new lastname",
                reply_markup=cancel_skip_kb
            )
    else:
        await message.answer(text="Please, send only text type message")


@setting_router.message(and_f(AdminsStates.adminFirstnameState))
async def modify_lastname_handler(message: Message, state: FSMContext):
    if message.text:
        if message.text == "Cancel":
            await state.set_state(StaffStates.admin)
            await message.answer(
                text='Canceled', reply_markup=kb_manage
            )
        elif message.text == "Skip":
            await state.update_data(lastname="None")
            await state.set_state(AdminsStates.adminUsernameState)
            await message.answer(
                text="Please, text new username",
                reply_markup=cancel_and_back
            )
        else:
            await state.update_data(lastname=message.text)
            await state.set_state(AdminsStates.adminUsernameState)
            await message.answer(
                text="Please, text new username",
                reply_markup=cancel_and_back
            )
    else:
        await message.answer(text="Please, send only text type message")


@setting_router.message(and_f(AdminsStates.adminUsernameState))
async def modify_username_handler(message: Message, state: FSMContext):
    if message.text:
        if message.text == "Cancel":
            await state.set_state(StaffStates.admin)
            await message.answer(
                text='Canceled', reply_markup=kb_manage
            )
        elif message.text == 'Back':
            await state.set_state(AdminsStates.adminFirstnameState)
            await message.answer(
                text="Please, text new lastname",
                reply_markup=cancel_skip_kb
            )
        else:
            await state.update_data(username=message.text)
            await state.set_state(AdminsStates.adminPasswordState)
            await message.answer(
                text="Please, text new password",
                reply_markup=cancel_and_back
            )
    else:
        await message.answer(text="Please, send only text type message")


@setting_router.message(AdminsStates.adminPasswordState)
async def modify_password_handler(message: Message, state: FSMContext):
    if message.text:
        if message.text == "Cancel":
            await state.set_state(StaffStates.admin)
            await message.answer(
                text='Canceled', reply_markup=kb_manage
            )
        elif message.text == "Back":
            await state.set_state(AdminsStates.adminUsernameState)
            await message.answer(
                text="Please, text new username",
                reply_markup=cancel_and_back
            )
        else:
            x = 0
            check_data = db.get_admin_list_all()
            all_data = await state.get_data()
            username = all_data.get('username')
            if all_data.get('admin_id'):
                await state.update_data(password=message.text)
                await state.set_state(AdminsStates.adminRuleState)
                await message.answer(
                    text="Please, send rule (only in digits 0 or 1)",
                    reply_markup=cancel_and_back
                )
            else:
                for check in check_data:
                    if username == check[7] or message.text == check[8]:
                        x +=1
                        await state.set_state(AdminsStates.adminUsernameState)
                        await message.answer(
                            text='Sorry, the login or password already existed',
                            reply_markup=cancel_and_back
                        )
                        break
                if x == 0:
                    await state.update_data(password=message.text)
                    await state.set_state(AdminsStates.adminRuleState)
                    await message.answer(
                        text="Please, send rule (only in digits 0 or 1)",
                        reply_markup=cancel_and_back
                    )
    else:
        await message.answer(text="Please, send only text type message")


@setting_router.message(and_f(AdminsStates.adminRuleState))
async def modify_rule_handler(message: Message, state: FSMContext):
    if message.text:
        if message.text == "Cancel":
            await state.set_state(StaffStates.admin)
            await message.answer(
                text='Canceled', reply_markup=kb_manage
            )
        elif message.text == "Back":
            await state.set_state(AdminsStates.adminPasswordState)
            await message.answer(
                text="Please, text new password",
                reply_markup=cancel_and_back
            )
        elif message.text.isdigit():
            if int(message.text) == 1 or int(message.text) == 0:
                await state.update_data(rule=int(message.text))
                await state.set_state(AdminsStates.shiftState)
                await message.answer(
                    text="Please, send new shift",
                    reply_markup=skip_back_cancel_kb
                )
            else:
                await message.answer("Please, send only 1 or 0 digit")
        else:
            await message.answer(text="Please, send only in digits 0 or 1)")
    else:
        await message.answer(text="Please, send only in digits 0 or 1)")


@setting_router.message(AdminsStates.shiftState)
async def modify_shift_handler(message: Message, state: FSMContext):
    if message.text:
        if message.text == "Cancel":
            await state.set_state(StaffStates.admin)
            await message.answer(
                text='Canceled', reply_markup=kb_manage
            )
        elif message.text == "Back":
            await state.set_state(AdminsStates.adminRuleState)
            await message.answer(
                text="Please, send rule (only in digits 0 or 1)",
                reply_markup=cancel_and_back
            )
        elif message.text == "Skip":
            await state.update_data(shift="None")
            await state.set_state(AdminsStates.tg_usernameState)
            await message.answer(
                text="Please, send new telegram",
                reply_markup=skip_back_cancel_kb
            )
        else:
            await state.update_data(shift=message.text)
            await state.set_state(AdminsStates.tg_usernameState)
            await message.answer(
                text="Please, send new telegram",
                reply_markup=skip_back_cancel_kb
            )
    else:
        await message.answer(text="Please, send only text type message")


@setting_router.message(and_f(AdminsStates.tg_usernameState))
async def modify_user_tg_handler(message: Message, state: FSMContext):
    if message.text:
        if message.text == "Cancel":
            await state.set_state(StaffStates.admin)
            await message.answer(
                text='Canceled', reply_markup=kb_manage
            )
        elif message.text == "Back":
            await state.set_state(AdminsStates.shiftState)
            await message.answer(
                text="Please, send new shift",
                reply_markup=skip_back_cancel_kb
            )
        elif message.text == "Skip":
            await state.update_data(tg_username="None")
            await state.set_state(AdminsStates.contactState)
            await message.answer(
                text="Please, send new contact",
                reply_markup=skip_back_cancel_kb
            )
        else:
            await state.update_data(tg_username=message.text)
            await state.set_state(AdminsStates.contactState)
            await message.answer(
                text="Please, send new contact",
                reply_markup=skip_back_cancel_kb
            )
    else:
        await message.answer("Please, send only text and numeric type message")


@setting_router.message(and_f(AdminsStates.contactState))
async def modify_contact_handler(message: Message, state: FSMContext):
    all_data = await state.get_data()
    if all_data.get('admin_id') is not None:
        admin_id = all_data['admin_id']
    else:
        admin_id = None
    first_name = all_data['first_name']
    lastname = all_data['lastname']
    username = all_data['username']
    password = all_data['password']
    rule = all_data['rule']
    shift = all_data['shift']
    tg_username = all_data['tg_username']

    s = ""
    if message.text:
        if message.text == "Cancel":
            await state.set_state(StaffStates.admin)
            await message.answer(
                text='Canceled', reply_markup=kb_manage
            )
        elif message.text == "Back":
            await state.set_state(AdminsStates.tg_usernameState)
            await message.answer(
                text="Please, send new telegram"
            )
        elif message.text == "Skip":
            await state.update_data(contact="None")
            await state.set_state(AdminsStates.saveState)
            get_contact = await state.get_data()
            contact = get_contact['contact']
            s += f"<b>ID:</b> {admin_id}\n"
            s += f"<b>Firstname:</b> {first_name}\n"
            s += f"<b>Lastname:</b> {lastname}\n"
            s += f"<b>Username:</b> {username}\n"
            s += f"<b>Password:</b> {password}\n"
            s += f"<b>Rule:</b> {rule}\n"
            s += f"<b>Shift:</b> {shift}\n"
            s += f"<b>Telegram:</b> {tg_username}\n"
            s += f"<b>Contact:</b> {contact}\n"

            await message.answer(
                text=f"{s}\nDo you want to save",
                reply_markup=make_confirm_kb(),
            )
        else:
            await state.update_data(contact=message.text)
            await state.set_state(AdminsStates.saveState)

            s += f"<b>ID:</b> {admin_id}\n"
            s += f"<b>Firstname:</b> {first_name}\n"
            s += f"<b>Lastname:</b> {lastname}\n"
            s += f"<b>Username:</b> {username}\n"
            s += f"<b>Password:</b> {password}\n"
            s += f"<b>Rule:</b> {rule}\n"
            s += f"<b>Shift:</b> {shift}\n"
            s += f"<b>Telegram:</b> {tg_username}\n"
            s += f"<b>Contact:</b> {message.text}\n"

            await message.answer(
                text=f"{s}\nDo you want to save",
                reply_markup=make_confirm_kb(),
            )
    else:
        await message.answer(text="Please, send only contact")


@setting_router.callback_query(AdminsStates.saveState)
async def modified_admin_save_handler(query: CallbackQuery, state: FSMContext):
    if query.data == "YES":
        all_data = await state.get_data()
        # add_admin = all_data['add_admin']

        first_name = all_data.get('first_name')
        lastname = all_data.get('lastname')
        username = all_data.get('username')
        password = all_data.get('password')
        rule = all_data.get('rule')
        shift = all_data.get('shift')
        tg_username = all_data.get('tg_username')
        contact = all_data['contact']
        if all_data.get('admin_id') is not None:
            admin_id = all_data.get('admin_id')
            db.add_admin(
                fname=first_name,
                lname=lastname,
                username=username,
                password=password,
                rule=rule,
                tg_username=tg_username,
                contact=contact,
                shift=shift,
                user_id=admin_id
            )
            await query.message.delete()
            await query.message.answer(
                text="Successfully edited",
                reply_markup=kb_manage
            )
        else:
            db.add_admin(
                fname=first_name,
                lname=lastname,
                username=username,
                password=password,
                rule=rule,
                tg_username=tg_username,
                contact=contact,
                shift=shift
            )
            await query.message.delete()
            await query.message.answer(
                text="Successfully added",
                reply_markup=kb_manage
            )
        await state.clear()
    else:
        await state.set_state(StaffStates.admin)
        await query.message.delete()
        await query.message.answer(
            text='All action canceled', reply_markup=kb_manage
        )
    await state.set_state(StaffStates.admin)


# add admin
@setting_router.message(and_f(F.text == 'Add admin', StaffStates.admin))
async def add_admin_handler(message: Message, state: FSMContext):
    await state.set_state(AdminsStates.editAdminState)
    await state.update_data(add_admin='add_admin')
    await message.answer(
        text=f"Please, enter new firstname...",
        reply_markup=cancel
    )


# work with log out button
@setting_router.message(and_f(F.text == 'Log out', StaffStates.admin))
async def logout_handler(message: Message, state: FSMContext):
    await message.answer(text='Logged out', reply_markup=kb_info)
    await message.bot.set_my_commands(commands=[
        BotCommand(command='start', description='Start/restart bot')
    ])
    await state.clear()
