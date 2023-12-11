import datetime
from aiogram.types import Message, InputFile
from admin_panel.PATH import TEMP
from admin_panel.entities.user import User
from admin_panel.entities.smart_time import Time
from admin_panel.database import db_sending
from prettytable import PrettyTable

class Sending:

    def __init__(self, message: Message):
        self.message = message
        self.start_time = None
        self.end_time = None
        self.during = None
        self.success = 0
        self.failure = 0

    async def start(self):
        self.start_time = datetime.datetime.now()
        for user in User.users():
            try:
                await self.message.copy_to(chat_id=user[0])
                self.success += 1
            except Exception:
                self.failure += 1
        self.end_time = datetime.datetime.now()
        self.during = str(Time(t1=self.start_time, t2=self.end_time))
        self._make_log()

    def _make_log(self):
        db_sending.insert({
            "start_time": self.start_time,
            "end_time": self.end_time,
            "during": self.during,
            "success": self.success,
            "failure": self.failure
        })

    @classmethod
    def sendings(cls):
        return db_sending.get_all()

    @classmethod
    def collect_data(cls, proj_name):
        table = PrettyTable(["[SUCCESS]", "[ERROR]", "Длительность", "Начало", "Конец"])
        table.set_style(15)
        table.title = f"Информация о проведённых рассылках в проекте @{proj_name}"
        for row in db_sending.get_all():
            table.add_row([row[3], row[4], row[2], row[0], row[1]])
        _path = TEMP + "sending_info.txt"
        with open(_path, "w", encoding = "utf-8") as f:
            f.write(str(table))
        return InputFile(_path)