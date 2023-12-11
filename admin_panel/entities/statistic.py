import datetime

from aiogram.types import InputFile
from prettytable import PrettyTable
from admin_panel.database import db_sending, db_users
from admin_panel.PATH import TEMP

class Statistic:
    users_online = 0
    users_all = 0
    users_banned = 0
    users_free = 0

    @classmethod
    def prepare_general(cls):
        cls.users_online = 0
        cls.users_all = 0
        cls.users_banned = 0
        cls.users_free = 0
        for i in db_users.get_all():
            cls.users_all += 1
            if (datetime.datetime.now() - datetime.datetime.fromisoformat(i[4])).total_seconds() < 300:
                cls.users_online += 1
            if datetime.datetime.now() > datetime.datetime.fromisoformat(i[3]):
                cls.users_free += 1
            else:
                cls.users_banned += 1

    @classmethod
    def collect_general(cls):
        cls.prepare_general()
        table = PrettyTable(["Параметр", "Значение"])
        table.title = f"Основные показатели статистики в проекте"
        table.set_style(15)
        table.encoding = "utf-8"
        path = TEMP + "general.txt"
        table.add_row(["Всего пользователей", cls.users_all])
        table.add_row(["Онлайн пользователей", cls.users_online])
        table.add_row(["Забаненных пользователей", cls.users_banned])
        table.add_row(["Свободных пользователей", cls.users_free])
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(table))
        return InputFile(path)

    @classmethod
    def collect_income(cls):
        table = PrettyTable(["Дата", "Новых пользователей"])
        table.set_style(15)
        table.title = f"Приход пользователей в проект"
        table.encoding = "utf-8"
        path = TEMP + "income.txt"
        sorted_data = {}
        for i in db_users.get_all():
            try:
                sorted_data[i[2]] += 1
            except:
                sorted_data[i[2]] = 1
        for i in sorted_data:
            table.add_row([i, "+" + str(sorted_data[i]) + " пользователей"])
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(table))
        return InputFile(path)

