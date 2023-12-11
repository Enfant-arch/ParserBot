from aiogram.types import Message
from admin_panel.PATH import SETTINGS, TEMP
import os
import configparser


class Agreement:

    def __init__(self):
        self.path = TEMP + "agreement"

    @property
    def message(self) -> str:
        with open(self.path, encoding="utf-8") as f:
            return f.read()

    def edit_message(self, message: Message):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(message.text)

    @classmethod
    def turn_on(cls):
        config = configparser.ConfigParser()
        config.read(SETTINGS)
        config["SETTINGS"]["agreement"] = "TRUE"
        with open(SETTINGS, "w") as f:
            config.write(f)

    @classmethod
    def turn_off(cls):
        config = configparser.ConfigParser()
        config.read(SETTINGS)
        config["SETTINGS"]["agreement"] = "FALSE"
        with open(SETTINGS, "w") as f:
            config.write(f)


    def __bool__(self):
        if self.message == "":
            return False
        config = configparser.ConfigParser()
        config.read(SETTINGS)
        agreement = config["SETTINGS"]["agreement"]
        return agreement == "TRUE"