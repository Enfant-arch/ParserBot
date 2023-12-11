import re
from aiogram.dispatcher import FSMContext
import admin_panel.keyboard as kb
import admin_panel.state as st
from admin_panel.entities.admin import Admin
from admin_panel.entities.user import User
from admin_panel.panel.core import core
from aiogram.types import Message, CallbackQuery
from admin_panel.filters import IsAdmin, CallEqual


@core.dp.callback_query_handler(CallEqual("menu_black_list"), IsAdmin())
async def menu_black_list(call: CallbackQuery):
    await call.message.edit_text(f"<b>🆔 Ваш id: <code>{call.from_user.id}</code></b>\n\n"
                                 f"<b>◾ Вы админ, вы можете банить/разбанивать пользователей вашего проекта</b>\n\n")
    await call.message.edit_reply_markup(kb.menu_black_list())

@core.dp.callback_query_handler(CallEqual("ban_user"), IsAdmin())
async def ban_user(call: CallbackQuery):
    await call.answer("◾ Введите id пользователя, которого хотите забанить", show_alert=True)
    await st.BlackList.ban.set()

@core.dp.message_handler(state=st.BlackList.ban)
async def ban_user(message: Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data["user_id"] = int(message.text)
            data["during"] = 0
            await core.dp.bot.get_chat(data['user_id'])
            if data["user_id"] == core.main_admin or data["user_id"] in Admin.admins():
                await message.answer(f"<b>⚠ Нельзя забанить одного из админов проекта!</b>")
                await state.finish()
            else:
                await message.answer(f"<b>🆔 Целевое id:<code> {data['user_id']}</code></b>\n\n"
                                     f"<b>📆 Длительность бана:<code> {data['during']}h</code></b>",
                                     reply_markup=kb.ban_during())
    except Exception:
        await message.answer(f"<b>⚠ Был введён некорректный id!</b>")
        await state.finish()

@core.dp.callback_query_handler(state=st.BlackList.ban)
async def ban_user(call: CallbackQuery, state: FSMContext):
    if re.search(r"(minus|add|set)_\d+h", call.data):
        try:
            async with state.proxy() as data:
                value = call.data.replace("minus", "-").replace("add", "+").replace("_", "").replace("h", "").replace("set",
                                                                                                                      "")
                if "set" in call.data:
                    data["during"] = int(value)
                else:
                    new = eval(f"""{data['during']}{value}""")
                    data["during"] = new if new > 0 else 0
                await call.message.edit_text(f"<b>🆔 Целевое id:<code> {data['user_id']}</code></b>\n\n"
                                             f"<b>📆 Длительность бана:<code> {data['during']}h</code></b>",
                                             reply_markup=kb.ban_during())
        except:
            await call.answer("⚠ Значение уже установлено!")
    elif call.data == "accept_ban":
        async with state.proxy() as data:
            user = User(data["user_id"])
            user.get_ban(data["during"])
            await call.message.answer(f"<b>✅ Пользователь<code> id{user.id} </code>был забанен до<code> {user.banned_for}</code>!</b>\n\n"
                                      f"<b>✅ Бот уведомил пользователя о бане!</b>")
            await core.dp.bot.send_message(chat_id=user.id,
                                           text=f"<b>😩 Вы были забанены админом проекта до <code>{user.banned_for}</code></b>")
            core.logger.make_log(f"{user.id} has been banned for {user.banned_for}", initiator=call.from_user.id)
            await call.message.delete()
        await state.finish()

@core.dp.callback_query_handler(CallEqual("unban_user"), IsAdmin())
async def unban_user(call: CallbackQuery):
    await call.answer("◾ Введите id пользователя, которого хотите разбанить", show_alert=True)
    await st.BlackList.unban.set()

@core.dp.message_handler(state=st.BlackList.unban)
async def unban_user(message: Message, state: FSMContext):
    try:
        user = User(message.text)
        user.get_unban()
        await message.answer("<b>✅ Пользователь был успешно разбанен!</b>")
        core.logger.make_log(f"{user.id} has been unbanned", initiator=message.from_user.id)
    except:
        await message.answer("<b>⚠ Введён некорректный id!</b>")
    finally:
        await state.finish()

@core.dp.message_handler(lambda message: User.is_banned(message.from_user.id))
async def catch_banned(message: Message):
    await message.answer(f"<b>😩 Вы были забанены админом проекта до<code> {User(message.from_user.id).banned_for}</code></b>")

@core.dp.callback_query_handler(lambda call: User.is_banned(call.from_user.id))
async def catch_banned(call: CallbackQuery):
    await call.message.answer(f"<b>😩 Вы были забанены админом проекта до<code> {User(call.from_user.id).banned_for}</code></b>")

@core.dp.message_handler(lambda message: not message.from_user.username)
async def catch_banned(message: Message):
    await message.answer(f"<b>⚠ Для использования бота установите username!</b>")

@core.dp.callback_query_handler(lambda call: not call.from_user.username)
async def catch_banned(call: CallbackQuery):
    await call.message.answer(f"<b>⚠ Для использования бота установите username!</b>")