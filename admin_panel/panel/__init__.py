from aiogram.contrib.fsm_storage.memory import MemoryStorage
from admin_panel.panel.core import Dispatcher, core
from admin_panel.middleware import UserUpdater

class Panel:
    def __init__(self,
                 main_admin: int,
                 dispatcher: Dispatcher,
                 update_username: bool = False,
                 update_activity: bool = False):
        self.core = core
        self.core.main_admin = int(main_admin)
        self.core.update_activity = update_activity
        self.core.update_username = update_username
        dispatcher.storage = MemoryStorage()
        dispatcher.bot.parse_mode = "html"
        dispatcher.setup_middleware(UserUpdater())
        self.core.dp = dispatcher

    def start(self):
        from admin_panel import handlers
        import asyncio
        self.core.logger.make_log(f"User id{self.core.main_admin} was authorized as MAIN ADMIN")
        self.core.logger.make_log(f"Updating usernames is turn {'on' if self.core.update_username else 'off'}")
        self.core.logger.make_log(f"Updating activity is turn {'on' if self.core.update_activity else 'off'}")
        self.core.logger.send_divider()
        return self
