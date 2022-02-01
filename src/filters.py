import telebot
from src.bot import bot

class IsAdmin(telebot.SimpleCustomFilter):
    """
    Class will check wether the user is admin or creater in group or not
    """
    key = 'is_admin'
    @staticmethod
    def check(message: telebot.types.Message):
        return bot.get_chat_member(message.chat.id, message.from_user.id).status in ['administrator', 'creator']

