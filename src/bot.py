import os

import telebot


# Initialize bot
bot =  telebot.TeleBot(
    os.environ['TELEGRAM_BOT_TMP_TOKEN'], parse_mode='HTML'
    )

