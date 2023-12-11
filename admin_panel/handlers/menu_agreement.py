from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from admin_panel.entities.user import User
from admin_panel.filters import CallEqual, AcceptAgreement, IsAdmin
from admin_panel.panel import core
import admin_panel.keyboard as kb
from loader import dp, bot
from data import config
import admin_panel.state as st


@core.dp.callback_query_handler(CallEqual("menu_agreement"), IsAdmin())
async def menu_agreement(call: CallbackQuery):
    await call.message.edit_text(f"<b>🆔 Ваш id: <code>{call.from_user.id}</code></b>\n\n"
                                 "<b>◾ Здесь вы можете редактировать текст пользовательского соглашения, а также включать/выключать его!</b>",
                                 reply_markup=kb.menu_agreement())


@core.dp.callback_query_handler(CallEqual("turn_off_agreement"), IsAdmin())
async def turn_off_agreement(call: CallbackQuery):
    core.agreement.turn_off()
    await call.message.edit_reply_markup(kb.menu_agreement())


@core.dp.callback_query_handler(CallEqual("turn_on_agreement"), IsAdmin())
async def turn_on_agreement(call: CallbackQuery):
    core.agreement.turn_on()
    try:
        await call.message.edit_reply_markup(kb.menu_agreement())
    except:
        await call.answer("⚠ Невозможное действие, так как соглашение не добавлено!")


@core.dp.callback_query_handler(CallEqual("edit_agreement"), IsAdmin())
async def edit_agreement(call: CallbackQuery):
    await call.message.answer(
        "<b>◾ Введите сообщение-соглашение поддерживается только текстовый формат, поддерживаются<code> html-теги</code></b>",
        reply_markup=kb.close())
    await st.Agreement.edit.set()


@core.dp.message_handler(IsAdmin(), state=st.Agreement.edit)
async def start_agreement(message: Message, state: FSMContext):
    core.agreement.edit_message(message)
    await message.reply("<b>✅ Сообщение было успешно установлено!</b>")
    await state.finish()


@core.dp.callback_query_handler(CallEqual("show_agreement"), IsAdmin())
async def show_agreement(call: CallbackQuery):
    if core.agreement:
        await call.message.answer(text=core.agreement.message)
    else:
        await call.answer("⚠ Невозможное действие, так как соглашение не добавлено!")


@core.dp.message_handler(AcceptAgreement())
async def start_agreement(message: Message):
    await message.answer(text=core.agreement.message,
                         reply_markup=kb.accept_agreement())
    await bot.send_sticker(chat_id=message.from_user.id, sticker=config.sticker_agreement)


@core.dp.callback_query_handler(CallEqual("accept_agreement"), AcceptAgreement())
async def menu_agreement(call: CallbackQuery):
    User(call.from_user.id).accept_agreement()
    await call.message.answer("<b>✅ Соглашение успешно принято!\n\n</b>"
                              "<b>◾ Введите /start для работы с ботом!</b>")
    await call.message.delete()
    call.message.to_python()


@core.dp.message_handler(commands=["rule", "rules", "agreement"])
async def rules(message: Message):
    if core.agreement:
        await message.reply(core.agreement.message)
    else:
        await message.delete()
