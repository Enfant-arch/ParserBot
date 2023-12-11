from admin_panel.database import db_channels
from admin_panel.exception.channel import ChannelExistsError, ChannelLimitError, BotAdminError

class Channel:

    def __init__(self, channel_id):
        self.id = int(channel_id)
        self._s = ["channel_id", self.id]

    @property
    def invite_link(self):
        return db_channels.get(["invite_link"], self._s)[0][0]

    @classmethod
    def count(cls):
        return len(db_channels.get_all())

    @classmethod
    def is_new(cls, channel_id):
        if db_channels.get(["*"], ["channel_id", int(channel_id)]):
            return False
        return True

    @classmethod
    async def add(cls, channel_id, bot):
        name = (await bot.get_me()).username
        if not cls.is_new(channel_id=channel_id):
            raise ChannelExistsError
        if cls.count() >= 5:
            raise ChannelLimitError
        try:
            invite_link = await bot.create_chat_invite_link(chat_id=int(channel_id), name=name)
            db_channels.insert({
                "channel_id": int(channel_id),
                "invite_link": invite_link.invite_link
            })
        except:
            raise BotAdminError

    @classmethod
    def delete(cls, channel_id):
        if cls.is_new(channel_id):
            raise ChannelExistsError
        db_channels.delete(["channel_id", int(channel_id)])

    @classmethod
    def channels(cls):
        return [[i[0], i[1]] for i in db_channels.get_all()]