import os
import telebot
from message_handlers import start_handler, help_handler, info_handler, default_handler
from concurrent.futures import ThreadPoolExecutor

# Retrieving the bot token from environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Creating a telebot instance
bot = telebot.TeleBot(BOT_TOKEN)

# Creating a ThreadPoolExecutor instance for handling video download tasks
executor = ThreadPoolExecutor(max_workers=5)

# Download queue for each chat/user
download_queues = {}

# Menu for commands
menu = telebot.types.ReplyKeyboardMarkup()
menu.row("/start \U000025B6", "/info \U00002139", "/help \U00002754")


@bot.message_handler(commands=['start', 'hello', 'Start', 'Hello'])
def start(message):
    """
    Handle /start command.
    """
    start_handler(bot, message)


@bot.message_handler(commands=['help','Help'])
def help(message):
    """
    Handle /help command.
    """
    help_handler(bot, message, menu)


@bot.message_handler(commands=['info','Info'])
def info(message):
    """
    Handle /info command.
    """
    info_handler(bot, message)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """
    Handle all other messages that are not commands.
    """
    # Checking if there's already a download in progress for the chat
    if message.chat.id in download_queues and not download_queues[message.chat.id].done():
        bot.send_message(message.chat.id, 'There is already a download in progress. Please wait until it is completed.')
        return

    default_handler(bot, message)


if __name__ == '__main__':
    bot.polling()
