from aiogram.dispatcher.filters import Filter
from aiogram.types import Message

class MessEqual(Filter):
    def __init__(self, text):
        self._check_current = False
        self._chat_ids = None
        self._text = text

    @classmethod
    def validate(cls, full_config):
        return {}

    async def check(self, obj) -> bool:
        if isinstance(obj, Message):
            return self._text == obj.text
        return False

class MessStart(Filter):
    def __init__(self, text):
        self._check_current = False
        self._chat_ids = None
        self._text = text

    @classmethod
    def validate(cls, full_config):
        return {}

    async def check(self, obj) -> bool:
        if isinstance(obj, Message):
            return obj.text.startswith(self._text)
        return False

class MessEnd(Filter):
    def __init__(self, text):
        self._check_current = False
        self._chat_ids = None
        self._text = text

    @classmethod
    def validate(cls, full_config):
        return {}

    async def check(self, obj) -> bool:
        if isinstance(obj, Message):
            return obj.text.endswith(self._text)
        return False