import datetime
import os
from sys import platform

from aiogram.types import InputFile

from admin_panel.PATH import LOGS

class Logger:

    def __init__(self):
        self.clean()

    @staticmethod
    def start_message(bot_name: str):
        Logger.make_log(f"@{bot_name} has been started")

    @staticmethod
    def send_divider():
        now = datetime.datetime.now().replace(microsecond=0)
        with open(LOGS, "a", encoding="UTF-8") as f:
            f.write("==============================================================================\n")
        print("\033[0m\033[33m\033[40m" + "==============================================================================")

    @staticmethod
    def logs(text=False):
        if text:
            with open(LOGS, "r", encoding="UTF-8") as f:
                return f.read()
        return InputFile(LOGS)

    @staticmethod
    def clean():
        with open(LOGS, "w", encoding="UTF-8") as f:
            f.write("")
        if "window" in platform:
            os.system("cls")
        elif "linux" in platform:
            os.system("clear")


    @staticmethod
    def make_log(message, initiator=None):
        now = datetime.datetime.now().replace(microsecond=0)
        log1 = f"[{now}] "
        log2 = ""
        log3 = f"{message}"
        if initiator:
            log2 = f"id{initiator}: "
        with open(LOGS, "a", encoding="UTF-8") as f:
            f.write(log1 + log2 + log3 + "\n")
        print("\033[0m\033[33m\033[40m" + log1 + log2 + "\033[37m\033[4m" + log3)