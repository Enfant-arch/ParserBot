import re
from aiogram.dispatcher import FSMContext
import admin_panel.keyboard as kb
import admin_panel.state as st
from admin_panel.panel.core import core
from aiogram.types import Message, CallbackQuery
from admin_panel.filters import IsAdmin, CallEqual, CallStart
from admin_panel.entities.sending import Sending

@core.dp.callback_query_handler(CallEqual("menu_sending"), IsAdmin())
async def menu_sending(call: CallbackQuery):
    await call.message.edit_text(f"<b>🆔 Ваш id: <code>{call.from_user.id}</code></b>\n\n"
                                 f"<b>◾ Вы <code>владелец</code>, вы можете делать рассылки!</b>\n\n")
    await call.message.edit_reply_markup(kb.menu_sending())

@core.dp.callback_query_handler(CallEqual("start_sending"), IsAdmin())
async def start_sending(call: CallbackQuery):
    await call.answer("Отправьте боту сообщение для рассылки, либо перешлите его, либо ответьте на желаемое сообщение /spam",
                      show_alert=True)
    await st.Sending.start.set()

@core.dp.message_handler(state=st.Sending.start)
async def start_sending(message: Message, state: FSMContext):
    letter = None
    if message.reply_to_message and message.text:
        if message.text == "/spam":
            letter = message.reply_to_message
    if not letter:
        letter = message
    await letter.reply("<b>🤨 Вы уверены?</b>",
                       reply_markup=kb.accept_sending())
    await state.finish()

@core.dp.callback_query_handler(CallEqual("accept_start_sending"), IsAdmin())
async def accept_start_sending(call: CallbackQuery):
    sending = Sending(call.message.reply_to_message)
    await call.message.answer("<b>✅ Рассылка началась!</b>")
    await sending.start()
    await call.message.answer(f"<b>✅ Рассылка закончилась, она заняла <code>{sending.during}</code></b>\n\n"
                              f"<b>👥 Пользователи:</b>\n\n"
                              f"<b>◾ Получили сообщение:<code> {sending.success}</code></b>\n"
                              f"<b>◾ Ошибка при отправке:<code> {sending.failure}</code></b>")
    core.logger.make_log(f"Sending has been finished  {sending.success}-[OK]  {sending.failure}-[ERROR]", initiator=call.from_user.id)
    await call.message.delete()

@core.dp.callback_query_handler(CallEqual("add_button"), IsAdmin())
async def add_button(call: CallbackQuery):
    await call.message.answer("<b>◾ Введите текст для кнопки в качестве ответа на сообщение, к которому хотите добавить кнопку...</b>")
    await st.AddButton.text.set()

@core.dp.message_handler(lambda message: message.reply_to_message, state=st.AddButton.text)
async def start_sending(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
        data["message"] = message.reply_to_message
    await message.answer("<b>◾ Введите ссылку для кнопки...</b>")
    await st.AddButton.next()

@core.dp.message_handler(state=st.AddButton.url)
async def start_sending(message: Message, state: FSMContext):
    if re.search(r"(https|http|www)://", message.text):
        async with state.proxy() as data:
            data["url"] = message.text
            await data['message'].reply(f"<b>◾ Текст для кнопки:<code> {data['text']}</code></b>\n\n"
                                        f"<b>◾ Ссылка для кнопки:<code> {data['url']}</code></b>\n\n",
                                        reply_markup=kb.accept_button())
    else:
        await message.answer("<b>⚠ Введена некорректная ссылка!</b>")
        await state.finish()


@core.dp.callback_query_handler(CallStart("accept_add_button"), state=st.AddButton.url)
async def start_sending(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        url = data['url']
        text = data['text']
        message: Message = data['message']

    await message.copy_to(chat_id=call.from_user.id,
                          reply_markup=kb.new_buttons(message.reply_markup, [text, url], insert=call.data.replace("accept_add_button_", "") == "2"))
    await call.message.delete()
    await state.finish()