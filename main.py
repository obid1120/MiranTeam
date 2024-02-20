import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from handlers.command_handlers import cmd_router
from handlers.message_handler import message_router


async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    db = Dispatcher()
    db.include_routers(cmd_router, message_router)
    await db.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except:
        print("Bot stopped")
