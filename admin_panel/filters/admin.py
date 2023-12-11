from aiogram.dispatcher.filters import Filter
from aiogram.types import Message

from admin_panel.entities.admin import Admin
from admin_panel.panel import core


class IsAdmin(Filter):

    async def check(self, obj) -> bool:
        user_id = obj.from_user.id
        if int(user_id) in Admin.admins():
            return True
        return user_id == core.main_admin


class AdminCommand(Filter):
    _command = None

    async def check(self, obj) -> bool:
        if isinstance(obj, Message):
            self._command = obj.text.lower()
            return self.seek()
        return False

    def seek(self):
        from re import search
        if search(r"a.?d.?m.?i.?n.?", self._command):
            return True
        elif search(r"а.?д.?м.?и.?н.?", self._command):
            return True
        elif search(r"ф.?в.?ь.?ш.?т.?", self._command):
            return True
        elif search(r"f.?l.?v.?b.?y.?", self._command):
            return True
        else:
            return False