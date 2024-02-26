from aiogram.types import BotCommand

manage_commands = [
    BotCommand(command='start', description='Start/restart bot'),
    BotCommand(command='admins_list', description='All admins list'),
    BotCommand(command='add_admin', description='Add new admin'),
    BotCommand(command='modify_admin', description='Update any admin'),
    BotCommand(command='del_admin', description='Remove any admin')
]

admin_commands = [
    BotCommand(command='start', description='Start/restart bot'),
    BotCommand(command='admins_list', description='All admins list'),
    BotCommand(command='modify_profile', description='Update personal profile'),
]