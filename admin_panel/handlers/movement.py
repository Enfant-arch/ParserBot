from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from admin_panel.panel.core import core
from admin_panel.filters import AdminCommand, IsAdmin, CallEqual
from admin_panel.keyboard import menu

@core.dp.message_handler(AdminCommand(), IsAdmin())
async def open_menu(message: Message):
    status = "владелец" if message.from_user.id == core.main_admin else "админ"
    await message.answer(f"<b>👋🏻 Приветствую тебя, <u>{message.from_user.full_name}</u></b>\n\n"
                         f"<b>◾ Ваш статус: <code>{status}</code></b>\n\n"
                         "<i>🖥 Пользуйтесь админ-панелью с удовольствием</i>\n\n",
                         reply_markup=menu())
    await message.delete()

@core.dp.callback_query_handler(CallEqual("to_menu"), IsAdmin())
async def to_menu(call: CallbackQuery):
    status = "владелец" if call.from_user.id == core.main_admin else "админ"
    await call.message.edit_text(f"<b>👋🏻 Приветствую тебя, <u>{call.from_user.full_name}</u></b>\n\n"
                                 f"<b>◾ Ваш статус: <code>{status}</code></b>\n\n"
                                 "<i>🖥 Пользуйтесь админ-панелью с удовольствием</i>\n",
                                 reply_markup=menu())

@core.dp.callback_query_handler(CallEqual("close"), state="*")
async def close(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()