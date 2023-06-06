import os
import telebot
from concurrent.futures import ThreadPoolExecutor
from message_handlers import start_handler, help_handler, info_handler, default_handler

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

executor = ThreadPoolExecutor(max_workers=5)

@bot.message_handler(commands=['start', 'hello', 'Start', 'Hello'])
def start(message):
    start_handler(bot, message)

@bot.message_handler(commands=['help','Help'])
def help(message):
    help_handler(bot, message)

@bot.message_handler(commands=['info','Info'])
def info(message):
    info_handler(bot, message)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    default_handler(bot, message, executor)

if __name__ == '__main__':
    bot.polling()
