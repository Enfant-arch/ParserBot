from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from admin_panel.panel.core import core
from admin_panel.filters import IsAdmin, CallEqual, CallStart
import admin_panel.keyboard as kb
from admin_panel.entities.admin import Admin, AdminExistsError, AdminLimitError
import admin_panel.state as st

@core.dp.callback_query_handler(CallEqual("menu_admins"), IsAdmin())
async def menu_admins(call: CallbackQuery):
    if call.from_user.id == core.main_admin:
        await call.message.edit_text(f"<b>🆔 Ваш id:<code> {call.from_user.id}</code></b>\n\n"
                                     f"<b>◾ Вы владелец, вы можете добавлять/удалять админов вашего проекта</b>\n\n"
                                     f"<b>◾ Лимит админов в проекте<code> 5 (не включая вас)</code></b>")
        await call.message.edit_reply_markup(kb.menu_admins([[i, "locked"] for i in Admin.admins()]))
    else:
        await call.answer("⚠ Вы не владелец, этот раздел вам недоступен!")

@core.dp.callback_query_handler(CallEqual("add_admin"), IsAdmin())
async def add_admin(call: CallbackQuery):
    await call.answer("◾ Введите ID админа, которого хотите добавить", show_alert=True)
    await st.Admin.add.set()

@core.dp.message_handler(IsAdmin(), state=st.Admin.add)
async def add_admin(message: Message, state: FSMContext):
    try:
        admin_id = int(message.text)
        if admin_id == core.main_admin:
            raise AdminExistsError
        await core.dp.bot.get_chat(admin_id)
        Admin.add(admin_id=admin_id)
        await message.answer("<b>✅ Добавлен новый админ!</b>\n\n"
                             f"<b>🆔 Его id: <code>{admin_id}</code></b>\n\n"
                             f"<code>✅ id{admin_id} </code><i>уже уведомлён о получении привелегий!</i>")
        await core.dp.bot.send_message(chat_id=admin_id,
                                       text="<b>🥳 Поздравляю вы получили статус <code>админ</code>!</b>\n\n"
                                            "<i>🖥 Для открытия админ-панели используйте команду <code>/admin</code> или <code>/админ</code></i>")
        core.logger.make_log(f"User id{admin_id} has become admin", initiator=core.main_admin)
    except AdminLimitError:
        await message.answer("<b>⚠ Админ добавлен не был!</b>\n\n"
                             "<i>🤷‍♂ Причина:</i><code> вы достигли лимита 5/5</code>")
    except AdminExistsError:
        await message.answer("<b>⚠ Админ добавлен не был!</b>\n\n"
                             "<i>🤷‍♂ Причина:</i><code> id уже в списке админов</code>")
    except Exception:
        await message.answer("<b>⚠ Админ добавлен не был!</b>\n\n"
                             "<i>🤷‍♂ Причина:</i><code> некорректный id</code>")
    finally:
        await state.finish()
        await message.delete()

@core.dp.callback_query_handler(CallEqual("refresh_admin"), IsAdmin())
async def refresh_admin(call: CallbackQuery):
    try:
        await call.message.edit_reply_markup(kb.menu_admins([[i, "locked"] for i in Admin.admins()]))
    except Exception:
        await call.answer("⚠ Ничего не изменилось!")

@core.dp.callback_query_handler(CallStart("unlock_delete_admin_"), IsAdmin())
async def unlock_delete_admin(call: CallbackQuery):
    admins = []
    for i in Admin.admins():
        if i == int(call.data.replace("unlock_delete_admin_", "")):
            admins.append([i, "unlocked"])
        else:
            admins.append([i, "locked"])
    await call.message.edit_reply_markup(kb.menu_admins(admins))

@core.dp.callback_query_handler(CallEqual("admin_locked"), IsAdmin())
async def admin_locked(call: CallbackQuery):
    await call.answer("⚠ Не доступно!")

@core.dp.callback_query_handler(CallStart("delete_admin_"), IsAdmin())
async def delete_admin(call: CallbackQuery):
    admin_id = int(call.data.replace("delete_admin_", ""))
    Admin.delete(admin_id)
    await call.message.edit_reply_markup(kb.menu_admins([[i, "locked"] for i in Admin.admins()]))
    await call.answer("✅ Админ успешно удалён!")
    core.logger.make_log(f"User id{admin_id} has been deleted from admin list", initiator=core.main_admin)