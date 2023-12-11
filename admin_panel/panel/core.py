from aiogram import Dispatcher
from admin_panel.entities.agreement import Agreement
from admin_panel.panel.logger import Logger
import logging
class Core:

    def __init__(self):
        self.main_admin: int = None
        self.dp: Dispatcher = None
        self.update_username = False
        self.update_activity = False
        self.logger = Logger()
        self.agreement = Agreement()

core = Core()
