import asyncio
import logging

from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from handlers.admin_handlers import user_router
from handlers.command_handlers import cmd_router
from handlers.message_handler import message_router
from handlers.update_handlers import update_handler
from handlers.manage_handlers import setting_router

PROXY = 'http://proxy.server:3128/'
session = AiohttpSession(proxy=PROXY)


async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML, session=session)
    await bot.set_my_commands(
        commands=[
            BotCommand(command='start', description='Start/restart bot')
        ]
    )
    db = Dispatcher()
    db.include_routers(cmd_router, message_router, update_handler, setting_router, user_router)
    await db.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except:
        print("Bot stopped")
