from aiogram.dispatcher.filters import Filter
from aiogram.types import CallbackQuery


class CallEqual(Filter):
    def __init__(self, text):
        self._check_current = False
        self._chat_ids = None
        self._text = text

    @classmethod
    def validate(cls, full_config):
        return {}

    async def check(self, obj) -> bool:
        if isinstance(obj, CallbackQuery):
            return self._text == obj.data
        return False


class CallStart(Filter):
    def __init__(self, text):
        self._check_current = False
        self._chat_ids = None
        self._text = text

    @classmethod
    def validate(cls, full_config):
        return {}
    async def check(self, obj) -> bool:
        if isinstance(obj, CallbackQuery):
            return obj.data.startswith(self._text)
        return False


class CallEnd(Filter):
    def __init__(self, text):
        self._check_current = False
        self._chat_ids = None
        self._text = text

    @classmethod
    def validate(cls, full_config):
        return {}

    async def check(self, obj) -> bool:
        if isinstance(obj, CallbackQuery):
            return obj.data.endswith(self._text)
        return False