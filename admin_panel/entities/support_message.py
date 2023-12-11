import datetime

from aiogram.types import User

from admin_panel.database import db_support_message

class From:
    def __init__(self, user_id, username):
        self.id = int(user_id)
        self.username = username

class SupportMessage:

    def __init__(self, unique_id: int):
        self.id = int(unique_id)
        self._s = ["unique_id", self.id]

    @property
    def from_user(self):
        data = db_support_message.get(["from_id", "from_username"], self._s)[0]
        return From(data[0], data[1])

    @property
    def sending_date(self):
        return datetime.datetime.fromisoformat(db_support_message.get(["sending_date"], self._s)[0][0]).replace(microsecond=0)

    @property
    def text(self):
        return db_support_message.get(["text"], self._s)[0][0]


    @classmethod
    def is_new(cls, unique_id):
        if len(db_support_message.get(["sending_date"], ["unique_id", unique_id])) == 0:
            return True
        return False

    @classmethod
    def create(cls, user: User, text: str):
        unique_id = str(datetime.datetime.now().timestamp()).split(".")[0]
        db_support_message.insert({
            "from_id": user.id,
            "from_username": user.username,
            "sending_date": datetime.datetime.now(),
            "text": text,
            "unique_id": unique_id
        })
        return SupportMessage(unique_id)

    @classmethod
    def delete(cls, unique_id):
        db_support_message.delete(["unique_id", int(unique_id)])

    @classmethod
    def clean(cls):
        for i in db_support_message.get_all():
            db_support_message.delete(["unique_id", int(i[4])])

    @classmethod
    def messages(cls):
        return db_support_message.get_all()

