from admin_panel.database.main import Database
from admin_panel.PATH import DB_PATH

db_channels = Database(table="channels", _db_path=DB_PATH + "channels.db").create_table({
    "channel_id": "INT",
    "invite_link": "TEXT"
})


db_admins = Database(table="admins", _db_path=DB_PATH + "admins.db").create_table({
    "admin_id": "INT"
})


db_users = Database(table="users", _db_path=DB_PATH + "users.db").create_table({
    "user_id": "INT",
    "username": "TEXT",
    "reg_date": "DATE",
    "banned_for": "TIME",
    "last_activity": "TIME",
    "agreement": "INT"
})


db_sending = Database(table="sending", _db_path=DB_PATH + "sending.db").create_table({
    "start_time": "TIME",
    "end_time": "TIME",
    "during": "TIME",
    "success": "INT",
    "failure": "INT"
})


db_support_message = Database(table="support", _db_path=DB_PATH + "support_message.db").create_table({
    "from_id": "INT",
    "from_username": "TEXT",
    "sending_date": "TIME",
    "text": "TEXT",
    "unique_id": "INT"
})