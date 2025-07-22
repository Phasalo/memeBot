import asyncio
from aiogram import Dispatcher

from config_data.config import bot
from config_data.middleware import setup_middlewares
from handlers import user_handlers, admin_handlers, commands, callbacks, inline_handler


async def main() -> None:
    dp = Dispatcher()
    setup_middlewares(dp)
    dp.include_router(admin_handlers.router)
    dp.include_router(commands.router)
    dp.include_router(user_handlers.router)
    dp.include_router(callbacks.router)
    dp.include_router(inline_handler.router)
    print("Phasalo Bot Template запущен!")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
