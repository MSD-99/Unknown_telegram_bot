from calendar import c
from sqlite3 import connect
import emoji
from loguru import logger

from src.bot import bot
from src.db import db
from src.filters import IsAdmin
from src.utils.constants import Keyboards, Keys, States
from src.utils.io import proxy, read_json, write_json


class Bot:
    """
    Template bot to connect two strangers randomly.
    """
    def __init__(self, Telebot) -> None:
        # self.proxy = '123.231.226.114:47562'
        # proxy(proxy_url=self.proxy, type='HTTPS')

        self.bot = Telebot

        # add mustom filter
        self.bot.add_custom_filter(IsAdmin())

        # register handler
        self.handlers()

        # run bot
        logger.info('Bot is running...')
        self.bot.infinity_polling()

        self.echo_all = self.bot.message_handler(
            func=lambda message: True)(self.echo_all)

    def handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            """
            Welcome Message
            """
            self.send_message(
                message.chat.id,
                f"Hey <strong> {message.chat.first_name} </strong>",
                reply_markup=Keyboards.main
                )

            db.users.update_one(
                {'chat.id': message.chat.id},
                {'$set': message.json},
                upsert=True
                )
            self.update_state(chat_id=message.chat.id, state=States.main)

        @self.bot.message_handler(regexp=emoji.emojize(Keys.random_connect))
        def random_connect(message):
            """
            Randomly connect to another user
            """
            self.send_message(
                message.chat.id,
                ':busts_in_silhouette: Connecting you to random stanger...',
                reply_markup=Keyboards.exit
                )
            self.update_state(
                chat_id=message.chat.id,
                state=States.random_connect
                )

            other_user = db.users.find_one(
                {
                    'state': States.random_connect,
                    'chat.id': {'$ne': message.chat.id}
                }
            )

            if not other_user:
                return

            # Update current other user state
            self.update_state(chat_id=other_user['chat']['id'], state=States.connected)
            self.send_message(
                chat_id=other_user['chat']['id'],
                text="Connected to anonymous stranger..."
                )
            # Update current user state
            self.update_state(message.chat.id, state=States.connected)
            self.send_message(
                chat_id=message.chat.id,
                text="Connected to anonymous stranger..."
                )

            # store Connected Users
            db.users.update_one(
                {'chat.id': message.chat.id},
                {'$set': {'connected_to': other_user['chat']['id']}}
            )

            db.users.update_one(
                {'chat.id': other_user['chat']['id']},
                {'$set': {'connected_to': message.chat.id}}
            )

        @self.bot.message_handler(regexp=emoji.emojize(Keys.exit))
        def exit(message):
            """
            Exit from chat or connecting state.
            """
            self.update_state(
                chat_id=message.chat.id,
                state=States.main
                )
            self.send_message(
                message.chat.id,
                Keys.exit,
                reply_markup=Keyboards.main
                )

            # get connected to user
            connected_to = db.users.find_one(
                {
                    'chat.id':  message.chat.id
                }
            )

            if not connected_to:
                return

            # Update Other user state and terminate the connection
            other_chat_id = connected_to['connected_to']
            self.update_state(chat_id=other_chat_id, state=States.main)

            # Send Message
            self.send_message(
                other_chat_id,
                f'{Keys.exit} from other one!',
                reply_markup=Keyboards.main
                )

            # Reomve Connected users
            db.users.update_one(
                {'chat.id': message.chat.id},
                {'$set': {'connected_to': None}}
            )
            db.users.update_one(
                {'chat.id': other_chat_id},
                {'$set': {'connected_to': None}}
            )

        @self.bot.message_handler(is_admin=True)
        def admin_of_group(message):
            """
            Admin Filter
            """
            self.send_message(
                message.chat.id,
                'You are admin of this group',
                )

        @self.bot.message_handler(func=lambda _: True)
        def echo(message):
            """
            Echo message to ther connected user
            """
            user = db.users.find_one(
                {'chat.id': message.chat.id}
            )

            if (
                (not user) or
                (user["state"] != States.connected) or
                (user['connected_to'] is None)
            ):
                return

            self.send_message(
                user['connected_to'],
                message.text,
            )

    def send_message(self, chat_id, text, reply_markup=None, emojize=True):
        """
        Send message to telegram bot.
        """
        if emojize:
            text = emoji.emojize(text, use_aliases=True)

        self.bot.send_message(chat_id, text, reply_markup=reply_markup)

    def update_state(self, chat_id, state):
        """
        Update User state.
        """
        db.users.update_one(
                {'chat.id': chat_id},
                {'$set': {'state': state}},
                upsert=True
                )


if __name__ == '__main__':
    logger.info('Bot started!')
    bot = Bot(Telebot=bot)
    bot.run()
