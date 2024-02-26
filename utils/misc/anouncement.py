from admin_panel.entities.admin import Admin
from loader import dp, bot

async def dll_in_market_changed():
    for i in Admin:
        await bot.send_message(chat_id=i, 
                               text="В маркете сменилась dll с товарами, обновите значение на актульное!")
