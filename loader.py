# - *- coding: utf- 8 - *-
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from admin_panel import Panel
from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot, storage=MemoryStorage())
Panel(
    main_admin=config.main_admin,
    dispatcher=dp
).start()