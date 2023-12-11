# - *- coding: utf- 8 - *-
import asyncio
from aiogram import executor
import filters
import middlewares
import logging
from handlers import dp
from utils.db_api.psql  import create_bdx, process_timer
from utils.other_func import on_startup_notify, update_last_profit, check_update_bot, update_profit, update_notifical_payment
from utils.set_bot_commands import set_default_commands

file_log = logging.FileHandler('WotShop.log', "a")
console_out = logging.StreamHandler()


logging.basicConfig(level=logging.INFO, handlers=(file_log, console_out), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def on_startup(dp):
    filters.setup(dp)
    middlewares.setup(dp)
    await set_default_commands(dp)
    await on_startup_notify(dp)
    asyncio.create_task(update_last_profit())
    asyncio.create_task(update_notifical_payment())
    asyncio.create_task(check_update_bot())
    logging.info("~~~~~ Bot was started ~~~~~")


if __name__ == "__main__":
    create_bdx()
    update_profit()
    executor.start_polling(dp, on_startup=on_startup)
